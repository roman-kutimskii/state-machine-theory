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
                machine[state]["transitions"][symbol] = row[i].split(",")

    return states[0], machine


def fill_epsilon(machine):
    epsilon = {}

    for state in machine:
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


def process_machine(input_file_name, output_file_name):
    initial_state, machine = read_machine_from_file(input_file_name)
    epsilon = fill_epsilon(machine)


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
