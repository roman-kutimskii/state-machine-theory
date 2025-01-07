from lexer_token import LexerToken
from simulator import Simulator
from token_type import token_types_map, TokenType

TOKEN_TYPES_LIST = token_types_map.values()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens: list[LexerToken] = []

    def tokenize(self) -> list[LexerToken]:
        while self.next_token():
            pass
        return self.tokens

    def next_token(self) -> bool:
        if self.pos >= len(self.text):
            return False
        for token_type in TOKEN_TYPES_LIST:
            simulator = Simulator(token_type.regex)
            result = simulator.run(self.text)
            if result:
                token = LexerToken(token_type.name, result, self.pos)
                self.pos += len(result)
                self.tokens.append(token)
                return True
        token = LexerToken(token_types_map.get("BAD"), self.text[self.pos], self.pos)
        self.pos += 1
        self.tokens.append(token)
