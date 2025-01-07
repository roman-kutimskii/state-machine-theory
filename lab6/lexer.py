from lexer_token import LexerToken


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = (0, 0)
        tokens: list[LexerToken] = []

    def tokenize(self) -> list[LexerToken]:
        return []