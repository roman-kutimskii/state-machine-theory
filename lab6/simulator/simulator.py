from .regex_to_nfa import process_regex
from .nfa_to_dfa import process_nfa
from .minimize import process_dfa


def convert_regex_to_dfa(regex):
    nfa = process_regex(regex)
    dfa = process_nfa(*nfa)
    machine = process_dfa(*dfa)
    return machine


class Simulator:
    def __init__(self, regex: str):
        self.machine = convert_regex_to_dfa(regex)

    def run(self, text: str) -> str:
        states, input_symbols, transitions, outputs, initial_state = self.machine

        result = ""
        current_state = initial_state
        for symbol in text:
            if symbol not in input_symbols:
                return result
            result += symbol
            if outputs[current_state] == "F":
                return result
