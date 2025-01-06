class TokenType:
    def __init__(self, name: str, regex: str):
        self.name = name
        self.regex = regex


token_types_list = {
    'NUMBER': TokenType('NUMBER', '[0-9]*'),
    'VARIABLE': TokenType('VARIABLE', '[а-я]*'),
    'SEMICOLON': TokenType('SEMICOLON', ';'),
    'SPACE': TokenType('SPACE', '[ \\n\\t\\r]'),
    'ASSIGN': TokenType('ASSIGN', 'РАВНО'),
    'LOG': TokenType('LOG', 'КОНСОЛЬ'),
    'PLUS': TokenType('PLUS', 'ПЛЮС'),
    'MINUS': TokenType('MINUS', 'МИНУС'),
    'LPAR': TokenType('LPAR', '\\('),
    'RPAR': TokenType('RPAR', '\\)'),
}
