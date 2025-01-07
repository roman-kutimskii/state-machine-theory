from token_type import TokenType


class LexerToken:
    def __init__(self, type: TokenType, value: str, pos: (int, int)):
        self.type = type
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f'{self.type} ({self.pos}) "{self.value}"'