import csv
import sys


def parse_regex(regex):
    machine = {
        'ss': {},
        'sf': {}
    }

    literal = regex[0]
    machine['s0'] = {}
    machine['ss'][literal] = 's0'

    literal = regex[1]
    machine['s1'] = {}
    machine['s0'][literal] = 's1'

    literal = regex[2]
    machine['s1'][literal] = 'sf'



    return machine


def write_machine(machine, output_file_name):
    symbols = set()
    for state in machine:
        transitions = machine[state]
        for symbol in transitions:
            symbols.add(symbol)

    finite_markers = [""]
    for state in machine:
        finite_markers.append("F" if state == "sf" else "")

    states = [""] + [state for state in machine]

    with open(output_file_name, 'w', newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(finite_markers)
        writer.writerow(states)
        for symbol in symbols:
            row = [symbol]
            for state in states[1:]:
                transition = ""
                if symbol in machine[state]:
                    transition = machine[state][symbol]
                row.append(transition)
            writer.writerow(row)


def process_regex(regex_pattern, output_file_name):
    machine = parse_regex(regex_pattern)
    write_machine(machine, output_file_name)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <output-file> <regex pattern>")
        return 1

    output_file_name = sys.argv[1]
    regex_pattern = sys.argv[2]

    try:
        process_regex(regex_pattern, output_file_name)
    except RuntimeError as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
