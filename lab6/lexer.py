from lexer_token import LexerToken
from simulator import Simulator
from token_type import token_types_map

TOKEN_TYPES_LIST = token_types_map.values()

SIMULATORS_MAP = {token.name: Simulator(token.regex) for token in TOKEN_TYPES_LIST}


class Lexer:
    def __init__(self, input_file: str):
        self.file = open(input_file, 'r', encoding='utf-8')

    def next_token(self) -> LexerToken:
        pass

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None
