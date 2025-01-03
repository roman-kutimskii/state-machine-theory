import csv
from pprint import pprint
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
                transitions.setdefault(states[index], {})[symbol] = row[index + 1].split('/')

    return states, inputs, transitions, initial_state


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
            pprint(values)
        elif machine_type == "moore":
            values = read_moore_machine(input_file_name)
        else:
            print(f"Unknown machine type: {machine_type}")
            return 1
    except RuntimeError as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
