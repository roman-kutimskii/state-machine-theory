import csv
import sys


class RegexNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"RegexNode({self.value})"


def is_sign(token):
    return token in "+*()|"


def parse_regex(expression):
    def parse(tokens):
        def get_next():
            return tokens.pop(0) if tokens else None

        def parse_primary():
            token = get_next()
            if not is_sign(token):
                return RegexNode(token)
            elif token == '(':
                node = parse_expression()
                if get_next() != ')':
                    raise ValueError("Mismatched parentheses")
                return node
            raise ValueError(f"Unexpected token: {token}")

        def parse_factor():
            node = parse_primary()
            while tokens and tokens[0] in ('*', '+'):
                op = get_next()
                node = RegexNode(op, left=node)
            return node

        def parse_term():
            node = parse_factor()
            while tokens and tokens[0] and (not is_sign(tokens[0]) or tokens[0] == '('):
                right = parse_factor()
                node = RegexNode('concat', left=node, right=right)
            return node

        def parse_expression():
            node = parse_term()
            while tokens and tokens[0] == '|':
                get_next()
                right = parse_term()
                node = RegexNode('|', left=node, right=right)
            return node

        return parse_expression()

    tokens = []
    for char in expression:
        tokens.append(char)

    return parse(tokens)


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
    tree = parse_regex(regex_pattern)
    # write_machine(machine, output_file_name)

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
