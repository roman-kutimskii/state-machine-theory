from lexer_token import LexerToken
from simulator import Simulator
from token_type import token_types_map

TOKEN_TYPES_LIST = token_types_map.values()

SIMULATORS_MAP = {token.name: Simulator(token.regex) for token in TOKEN_TYPES_LIST}


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: list[LexerToken] = []

    def tokenize(self) -> list[LexerToken]:
        while self.next_token():
            pass
        return list(filter(lambda token: token.type != "SPACE", self.tokens))

    def next_token(self) -> bool:
        if self.pos >= len(self.text):
            return False
        for token_type in TOKEN_TYPES_LIST:
            simulator = SIMULATORS_MAP.get(token_type.name)
            result = simulator.run(self.text[self.pos:])
            if result:
                token = LexerToken(token_type.name, result, (self.line, self.column))
                self.pos += len(result)
                self.column += len(result)
                if result == '\n':
                    self.line += 1
                    self.column = 1
                self.tokens.append(token)
                return True
        token = LexerToken("BAD", self.text[self.pos], (self.line, self.column))
        self.pos += 1
        self.column += 1
        self.tokens.append(token)
        return True
