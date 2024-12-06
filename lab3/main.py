import pprint
import re
import sys


def read_file_to_string(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except IOError:
        raise RuntimeError(f"Unable to open file: {file_path}")


def read_grammar(file_name, output_file_name):
    file_content = read_file_to_string(file_name)
    regex = re.compile(r"^\s*<(\w+)>\s*->\s*((?:<\w+>\s+)?[\wε](?:\s*\|\s*(?:<\w+>\s+)?[\wε])*)\s*$", re.MULTILINE)
    transition_regex = re.compile(r"^\s*(?:<(\w*)>)?\s*([\wε]*)\s*$")
    finite_state = None

    grammar = {}

    for grammar_match in regex.finditer(file_content):
        next_state = grammar_match.group(1)
        finite_state = finite_state if finite_state else next_state
        if grammar.get(next_state, None) is None:
            grammar[next_state] = {
                "is_finite": "F" if next_state == finite_state else "",
                "transitions": {}
            }
        transitions = grammar_match.group(2).split("|")
        for transition in transitions:
            transition_match = transition_regex.search(transition)
            symbol = transition_match.group(2)
            state = transition_match.group(1) if transition_match.group(1) is not None else "H"
            if grammar.get(state, None) is None:
                grammar[state] = {
                    "is_finite": "F" if state == finite_state else "",
                    "transitions": {symbol: [next_state]}
                }
            else:
                if grammar.get(state).get("transitions").get(symbol, None) is None:
                    grammar.get(state).get("transitions")[symbol] = [next_state]
                else:
                    grammar.get(state).get("transitions").get(symbol).append(next_state)

    states = ['H'] + [state for state in grammar if state != 'H']
    symbols = set()

    for state in grammar:
        for symbol in grammar[state]['transitions']:
            symbols.add(symbol)

    symbols = sorted(symbols)

    csv_header1 = [''] + ['F' if grammar[state]['is_finite'] == 'F' else '' for state in states]
    csv_header2 = [''] + [f'q{i}' for i in range(len(states))]

    csv_rows = []
    state_index_map = {state: f'q{i}' for i, state in enumerate(states)}

    for symbol in symbols:
        row = [''] * (len(states) + 1)
        row[0] = symbol
        for state in states:
            state_index = states.index(state) + 1
            for next_state in grammar[state]['transitions'].get(symbol, []):
                if row[state_index]:
                    row[state_index] += "," + state_index_map[next_state]
                else:
                    row[state_index] = state_index_map[next_state]
        csv_rows.append(row)

    with open(output_file_name, "w", encoding="utf-8") as output_file:
        output_file.write(';'.join(csv_header1)+"\n")
        output_file.write(';'.join(csv_header2)+"\n")
        for row in csv_rows:
            output_file.write(';'.join(row)+"\n")


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input-file> <output-file>")
        return 1

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    read_grammar(input_file_name, output_file_name)

    return 0


if __name__ == "__main__":
    sys.exit(main())
