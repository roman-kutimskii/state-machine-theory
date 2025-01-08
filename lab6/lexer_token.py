class LexerToken:
    def __init__(self, lexer_type: str, value: str, pos: (int, int)):
        self.type = lexer_type
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f'{self.type} {self.pos} "{self.value}"'
