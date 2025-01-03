import csv
import sys


def read_moore_machine(file_name):
    states = []
    inputs = []
    transitions = {}
    outputs = {}
    initial_state = None

    with open(file_name, 'r', newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        outputs_row = list(reversed(next(reader)[1:]))
        states = next(reader)[1:]
        initial_state = states[0]
        for state in states:
            outputs[state] = outputs_row.pop()
        for row in reader:
            symbol = row[0]
            inputs.append(symbol)
            for index in range(len(row) - 1):
                transitions.setdefault(states[index], {})[symbol] = row[index + 1]

    return states, inputs, transitions, outputs, initial_state


def read_mealy_machine(file_name):
    states = []
    inputs = []
    transitions = {}
    initial_state = None

    with open(file_name, 'r', newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        states = next(reader)[1:]
        initial_state = states[0]
        for row in reader:
            symbol = row[0]
            inputs.append(symbol)
            for index in range(len(row) - 1):
                transitions.setdefault(states[index], {})[symbol] = row[index + 1].split('/') if (
                        "/" in row[index + 1]) else []

    return states, inputs, transitions, initial_state


def write_mealy_machine(file_name, states, inputs, transitions, initial_state):
    states = [initial_state] + list(filter(lambda x: x != initial_state, states))
    with open(file_name, 'w', newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([""] + states)
        for symbol in inputs:
            row = [symbol]
            for state in states:
                transition = transitions[state][symbol]
                row.append(f"{transition[0]}/{transition[1]}" if transition else "")
            writer.writerow(row)


def write_moore_machine(file_name, states, inputs, transitions, outputs, initial_state):
    states = [initial_state] + list(filter(lambda x: x != initial_state, states))
    with open(file_name, 'w', newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        outputs_row = [""]
        for state in states:
            outputs_row.append(outputs[state])
        writer.writerow(outputs_row)
        writer.writerow([""] + states)
        for symbol in inputs:
            row = [symbol]
            for state in states:
                row.append(transitions[state][symbol])
            writer.writerow(row)


def remove_unreachable_states_mealy(states, inputs, transitions, initial_state):
    reachable_states = set()
    to_visit = [initial_state]

    while to_visit:
        state = to_visit.pop()
        if state in reachable_states:
            continue
        reachable_states.add(state)

        for symbol in transitions[state]:
            transition = transitions[state][symbol]
            if transition:
                to_visit.append(transition[0])

    return list(filter(lambda x: x in reachable_states, states)), inputs, transitions, initial_state


def remove_unreachable_states_moore(states, inputs, transitions, outputs, initial_state):
    reachable_states = set()
    to_visit = [initial_state]

    while to_visit:
        state = to_visit.pop()
        if state in reachable_states:
            continue
        reachable_states.add(state)

        for symbol in transitions[state]:
            transition = transitions[state][symbol]
            if transition:
                to_visit.append(transition)

    return list(filter(lambda x: x in reachable_states, states)), inputs, transitions, outputs, initial_state


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <machine-type> <input-file> <output-file>")
        return 1

    machine_type = sys.argv[1]
    input_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    try:
        if machine_type == "mealy":
            values = read_mealy_machine(input_file_name)
            values = remove_unreachable_states_mealy(*values)
            write_mealy_machine(output_file_name, *values)
        elif machine_type == "moore":
            values = read_moore_machine(input_file_name)
            values = remove_unreachable_states_moore(*values)
            write_moore_machine(output_file_name, *values)
        else:
            print(f"Unknown machine type: {machine_type}")
            return 1
    except RuntimeError as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
