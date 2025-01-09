from lexer_token import LexerToken
from simulator import Simulator
from token_type import TOKEN_TYPES

SIMULATORS_MAP = {token.name: Simulator(token.regex) for token in TOKEN_TYPES}


class Lexer:
    def __init__(self, input_file: str):
        self.file = open(input_file, 'r', encoding='utf-8')

    def next_token(self) -> LexerToken | None:
        pass

    def close(self) -> None:
        if self.file is not None:
            self.file.close()
            self.file = None
