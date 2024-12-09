import csv
import sys


def read_machine_from_file(file_path):
    finite_state = None
    states = []
    machine = {}
    with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        finite_markers = next(reader)[1:]
        states = next(reader)[1:]
        finite_state = states[finite_markers.index("F")]
        for row in reader:
            symbol = row[0]
            for i in range(1, len(row)):
                state = states[i - 1]
                if state not in machine:
                    machine[state] = {
                        "is_finite": state == finite_state,
                        "transitions": {}
                    }
                machine[state]["transitions"][symbol] = list(filter(lambda x: x != '', row[i].split(",")))

    return states[0], finite_state, machine


def fill_epsilon(machine):
    epsilon = {}

    for state in machine:
        if "ε" not in machine[state]["transitions"]:
            continue
        transitions = machine[state]["transitions"]["ε"]
        visited = set()
        stack = [state]

        while stack:
            vertex = stack.pop()

            if vertex not in visited:
                visited.add(vertex)

                for neighbor in machine[vertex]["transitions"]["ε"]:
                    if neighbor:
                        stack.append(neighbor)

        epsilon[state] = list(visited)

    return epsilon


def get_dependencies(states, epsilon):
    dependencies = set()

    for state in states:
        dependencies.add(state)
        for transition in epsilon[state]:
            dependencies.add(transition)

    return list(dependencies)


def find_key_with_value(dictionary, new_value):
    for key, value in dictionary.items():
        if tuple(sorted(value)) == tuple(sorted(new_value)):
            return key

    return None


def create_new_machine(initial_state, finite_state, epsilon, machine):
    s_count = 0
    state_dependencies = {"s0": [initial_state]}
    states = ["s0"]
    new_machine = {}

    for state in states:
        s_count += 1

        new_machine[state] = {
            "is_finite": finite_state in get_dependencies(state_dependencies[state], epsilon),
            "transitions": {}
        }

        for symbol in filter(lambda x: x != "ε", machine[initial_state]["transitions"]):
            transitions = []
            for dependency in get_dependencies(state_dependencies[state], epsilon):
                transitions.extend(machine[dependency]["transitions"][symbol])
            transitions = list(set(transitions))
            key = find_key_with_value(state_dependencies, transitions)
            if key is None:
                key = f"s{s_count}"
                states.append(key)
                state_dependencies[key] = transitions
            new_machine[state]["transitions"][symbol] = key

    return new_machine


def write_machine(machine, file_path):
    symbols = set()
    for state in machine:
        transitions = machine[state]["transitions"]
        for symbol in transitions:
            symbols.add(symbol)

    finite_markers = [""]
    for state in machine:
        marker = machine[state]["is_finite"]
        finite_markers.append("F" if marker else "")

    states = [""] + [state for state in machine]

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(finite_markers)
        writer.writerow(states)
        for symbol in symbols:
            row = [symbol]
            for state in states[1:]:
                row.append(machine[state]["transitions"][symbol])
            writer.writerow(row)


def process_machine(input_file_name, output_file_name):
    initial_state, finite_state, machine = read_machine_from_file(input_file_name)
    epsilon = fill_epsilon(machine)
    new_machine = create_new_machine(initial_state, finite_state, epsilon, machine)
    write_machine(new_machine, output_file_name)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input-file> <output-file>")
        return 1

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    try:
        process_machine(input_file_name, output_file_name)
    except RuntimeError as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
