import csv
import sys


class RegexNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"RegexNode({self.value})"


class State:
    def __init__(self):
        self.transitions = {}
        self.epsilon_transitions = []

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

    def add_epsilon_transition(self, state):
        self.epsilon_transitions.append(state)


class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state


def is_literal(token):
    return token not in "+*()|" and token != "concat"


def parse_regex(expression):
    def parse(tokens):
        def get_next():
            return tokens.pop(0) if tokens else None

        def parse_primary():
            token = get_next()
            if is_literal(token):
                return RegexNode(token)
            elif token == "(":
                node = parse_expression()
                if get_next() != ")":
                    raise ValueError("Mismatched parentheses")
                return node
            raise ValueError(f"Unexpected token: {token}")

        def parse_factor():
            node = parse_primary()
            while tokens and tokens[0] in ("*", "+"):
                op = get_next()
                node = RegexNode(op, left=node)
            return node

        def parse_term():
            node = parse_factor()
            while tokens and tokens[0] and (is_literal(tokens[0]) or tokens[0] == "("):
                right = parse_factor()
                node = RegexNode("concat", left=node, right=right)
            return node

        def parse_expression():
            node = parse_term()
            while tokens and tokens[0] == "|":
                get_next()
                right = parse_term()
                node = RegexNode("|", left=node, right=right)
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

    with open(output_file_name, "w", newline="", encoding="utf-8") as csvfile:
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


def print_tree(node, level=0):
    if node is not None:
        print_tree(node.right, level + 1)
        print(" " * 4 * level + "->", node.value)
        print_tree(node.left, level + 1)


def build_nfa(node):
    if node is None:
        return None

    if is_literal(node.value):
        start = State()
        accept = State()
        start.add_transition(node.value, accept)
        return NFA(start, accept)
    elif node.value == "concat":
        left_nfa = build_nfa(node.left)
        right_nfa = build_nfa(node.right)
        left_nfa.accept_state.add_epsilon_transition(right_nfa.start_state)
        return NFA(left_nfa.start_state, right_nfa.accept_state)
    elif node.value == '|':
        start = State()
        accept = State()
        left_nfa = build_nfa(node.left)
        right_nfa = build_nfa(node.right)
        start.add_epsilon_transition(left_nfa.start_state)
        start.add_epsilon_transition(right_nfa.start_state)
        left_nfa.accept_state.add_epsilon_transition(accept)
        right_nfa.accept_state.add_epsilon_transition(accept)
        return NFA(start, accept)
    elif node.value == '*':
        start = State()
        accept = State()
        sub_nfa = build_nfa(node.left)
        start.add_epsilon_transition(sub_nfa.start_state)
        start.add_epsilon_transition(accept)
        sub_nfa.accept_state.add_epsilon_transition(sub_nfa.start_state)
        sub_nfa.accept_state.add_epsilon_transition(accept)
        return NFA(start, accept)
    elif node.value == '+':
        start = State()
        accept = State()
        sub_nfa = build_nfa(node.left)
        start.add_epsilon_transition(sub_nfa.start_state)
        sub_nfa.accept_state.add_epsilon_transition(sub_nfa.start_state)
        sub_nfa.accept_state.add_epsilon_transition(accept)
        return NFA(start, accept)

    raise ValueError(f"Unexpected node value: {node.value}")

def print_nfa(nfa):
    def print_state(state, visited, state_index):
        if state in visited:
            return
        visited.add(state)
        for symbol, states in state.transitions.items():
            for s in states:
                print(f"S{state_index[state]} --{symbol}--- S{state_index[s]}")
                print_state(s, visited, state_index)
        for s in state.epsilon_transitions:
            print(f"S{state_index[state]} --ε--- S{state_index[s]}")
            print_state(s, visited, state_index)

    state_index = {}
    index = 0
    def assign_indices(state):
        nonlocal index
        if state not in state_index:
            state_index[state] = index
            index += 1
            for symbol, states in state.transitions.items():
                for s in states:
                    assign_indices(s)
            for s in state.epsilon_transitions:
                assign_indices(s)

    assign_indices(nfa.start_state)

    print("NFA:")
    print_state(nfa.start_state, set(), state_index)

def process_regex(regex_pattern, output_file_name):
    tree = parse_regex(regex_pattern)
    # print_tree(tree)
    nfa = build_nfa(tree)
    print_nfa(nfa)
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
