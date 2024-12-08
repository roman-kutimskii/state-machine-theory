import re
import sys


def read_file_to_string(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except IOError as e:
        raise RuntimeError(f"Unable to open file: {file_path}") from e


def parse_left_hand_grammar(file_content):
    grammar_pattern = re.compile(
        r"^\s*<(\w+)>\s*->\s*((?:<\w+>\s+)?[\wε](?:\s*\|\s*(?:<\w+>\s+)?[\wε])*)\s*$",
        re.MULTILINE
    )
    transition_pattern = re.compile(r"^\s*(?:<(\w*)>)?\s*([\wε]*)\s*$")

    grammar = {}
    finite_state = None

    for match in grammar_pattern.finditer(file_content):
        state = match.group(1)
        finite_state = finite_state or state
        transitions = match.group(2).split("|")

        if state not in grammar:
            grammar[state] = {
                "is_finite": "F" if state == finite_state else "",
                "transitions": {}
            }

        for transition in transitions:
            trans_match = transition_pattern.search(transition)
            symbol = trans_match.group(2)
            next_state = trans_match.group(1) or "H"

            if next_state not in grammar:
                grammar[next_state] = {
                    "is_finite": "F" if next_state == finite_state else "",
                    "transitions": {symbol: [state]}
                }
            else:
                if symbol not in grammar[next_state]["transitions"]:
                    grammar[next_state]["transitions"][symbol] = [state]
                else:
                    grammar[next_state]["transitions"][symbol].append(state)

    return grammar


def generate_csv(grammar, output_file_name):
    states = ['H'] + [state for state in grammar if state != 'H']
    symbols = sorted({symbol for state in grammar for symbol in grammar[state]['transitions']})

    csv_header1 = [''] + ['F' if grammar[state]['is_finite'] == 'F' else '' for state in states]
    csv_header2 = [''] + [f'q{i}' for i in range(len(states))]
    state_index_map = {state: f'q{i}' for i, state in enumerate(states)}

    csv_rows = []
    for symbol in symbols:
        row = [''] * (len(states) + 1)
        row[0] = symbol
        for state in states:
            state_index = states.index(state) + 1
            transitions = grammar[state]['transitions'].get(symbol, [])
            row[state_index] = ",".join(state_index_map[next_state] for next_state in transitions)
        csv_rows.append(row)

    with open(output_file_name, "w", encoding="utf-8") as output_file:
        output_file.write(';'.join(csv_header1) + "\n")
        output_file.write(';'.join(csv_header2) + "\n")
        for row in csv_rows:
            output_file.write(';'.join(row) + "\n")


def process_grammar(input_file_name, output_file_name):
    file_content = read_file_to_string(input_file_name)
    grammar = parse_left_hand_grammar(file_content)
    generate_csv(grammar, output_file_name)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input-file> <output-file>")
        return 1

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    try:
        process_grammar(input_file_name, output_file_name)
    except RuntimeError as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
