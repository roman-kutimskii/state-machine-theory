from regex_to_nfa import process_regex
from nfa_to_dfa import process_nfa
from minimize import process_dfa


class Simulator:
    def __init__(self, regex):
        self.regex = regex

    def convert_regex_to_dfa(self):
        nfa = process_regex(self.regex)
        dfa = process_nfa(*nfa)
        machine = process_dfa(*dfa)
        return machine
