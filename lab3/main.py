import re
import sys


def read_file_to_string(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
            first_line = file_content.split("\n")[0].strip('|')
            return file_content, first_line
    except IOError as e:
        raise RuntimeError(f"Unable to open file: {file_path}") from e


def parse_right_hand_grammar(file_content):
    grammar_pattern = re.compile(
        r"^\s*<(\w+)>\s*->\s*([\wε](?:\s+<\w+>)?(?:\s*\|\s*[\wε](?:\s+<\w+>)?)*)\s*$",
        re.MULTILINE
    )
    transition_pattern = re.compile(r"^\s*([\wε]*)\s*(?:<(\w*)>)?\s*$")

    grammar = {}
    initial_state = None

    for match in grammar_pattern.finditer(file_content):
        state = match.group(1)
        initial_state = initial_state or state
        transitions = match.group(2).split("|")

        grammar["H"] = {"is_finite": "F", "transitions": {}}

        for transition in transitions:
            trans_match = transition_pattern.search(transition)
            symbol = trans_match.group(1)
            next_state = trans_match.group(2) or "H"

            if state not in grammar:
                grammar[state] = {
                    "is_finite": "",
                    "transitions": {symbol: [next_state]}
                }
            else:
                if symbol not in grammar[state]["transitions"]:
                    grammar[state]["transitions"][symbol] = [next_state]
                else:
                    grammar[state]["transitions"][symbol].append(next_state)

    return grammar, initial_state


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

    return grammar, "H"


def generate_csv(grammar, output_file_name, initial_state="H"):
    states = [initial_state] + [state for state in grammar if state != initial_state]
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


def get_parser(text):
    pattern = re.compile(
        r"^\s*<(\w+)>\s*->\s*([\wε](?:\s+<\w+>)?(?:\s*\|\s*[\wε](?:\s+<\w+>)?)*)\s*$",
        re.MULTILINE
    )
    if len(re.findall(pattern, text)) == text.count('->'):
        return parse_right_hand_grammar
    pattern = re.compile(
        r"^\s*<(\w+)>\s*->\s*((?:<\w+>\s+)?[\wε](?:\s*\|\s*(?:<\w+>\s+)?[\wε])*)\s*$",
        re.MULTILINE
    )
    if len(re.findall(pattern, text)) == text.count('->'):
        return parse_left_hand_grammar
    return parse_left_hand_grammar


def process_grammar(input_file_name, output_file_name):
    file_content, first_line = read_file_to_string(input_file_name)
    parser = get_parser(file_content)
    grammar, initial_state = parser(file_content)
    generate_csv(grammar, output_file_name, initial_state)


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
