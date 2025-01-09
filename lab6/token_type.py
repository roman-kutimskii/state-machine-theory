from constants import *


class TokenType:
    def __init__(self, name: str, regex: str):
        self.name = name
        self.regex = regex

    def __str__(self):
        return self.name


TOKEN_TYPES = [
    TokenType('BLOCK_COMMENT', f'{{({SYMBOL.replace('}|', '')})*}}'),
    TokenType('LINE_COMMENT', f'//({SYMBOL})*\n'),
    TokenType('ARRAY', '(A|a)(R|r)(R|r)(A|a)(Y|y)'),
    TokenType('BEGIN', '(B|b)(E|e)(G|g)(I|i)(N|n)'),
    TokenType('ELSE', '(E|e)(L|l)(S|s)(E|e)'),
    TokenType('END', '(E|e)(N|n)(D|d)'),
    TokenType('IF', '(I|i)(F|f)'),
    TokenType('OF', '(O|o)(F|f)'),
    TokenType('OR', '(O|o)(R|r)'),
    TokenType('PROGRAM', '(P|p)(R|r)(O|o)(G|g)(R|r)(A|a)(M|m)'),
    TokenType('PROCEDURE', '(P|p)(R|r)(O|o)(C|c)(E|e)(D|d)(U|u)(R|r)(E|e)'),
    TokenType('THEN', '(T|t)(H|h)(E|e)(N|n)'),
    TokenType('TYPE', '(T|t)(Y|y)(P|p)(E|e)'),
    TokenType('VAR', '(V|v)(A|a)(R|r)'),
    TokenType('MULTIPLICATION', '\\*'),
    TokenType('PLUS', '\\+'),
    TokenType('MINUS', '-'),
    TokenType('DIVIDE', '/'),
    TokenType('SEMICOLON', ';'),
    TokenType('COMMA', ','),
    TokenType('LEFT_PAREN', '\\('),
    TokenType('RIGHT_PAREN', '\\)'),
    TokenType('LEFT_BRACKET', '['),
    TokenType('RIGHT_BRACKET', ']'),
    TokenType('EQ', '='),
    TokenType('GREATER', '>'),
    TokenType('LESS', '<'),
    TokenType('LESS_EQ', '<='),
    TokenType('GREATER_EQ', '>='),
    TokenType('NOT_EQ', '<>'),
    TokenType('ASSIGN', ':='),
    TokenType('COLON', ':'),
    TokenType('DOT', '.'),
    TokenType('IDENTIFIER', f'({LETTER}|_)({LETTER_OR_DIGIT}|_)*'),
    TokenType('STRING', f'\'{SYMBOL}*\''),
    TokenType('FLOAT', f'{NUMBER}.{DIGIT}+'),
    TokenType('INTEGER', f'{NUMBER}'),
    TokenType('SPACE', f' |\n|\t|\r'),
]
