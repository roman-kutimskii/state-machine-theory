import csv
import sys


def read_machine_from_file(file_path):
    finite_state = None
    states = []
    transitions = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        finite_markers = next(reader)[1:]
        states = next(reader)[1:]
        finite_state = states[finite_markers.index('F')]
        for row in reader:
            symbol = row[0]
            for i in range(1, len(row)):
                if states[i-1] not in transitions:
                    transitions[states[i-1]] = {}
                if symbol not in transitions[states[i-1]]:
                    transitions[states[i-1]][symbol] = []
                transitions.get(states[i-1], {}).get(symbol, []).append(row[i])

    return finite_state, states, transitions


def process_machine(input_file_name, output_file_name):
    read_machine_from_file(input_file_name)


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


if __name__ == '__main__':
    sys.exit(main())
