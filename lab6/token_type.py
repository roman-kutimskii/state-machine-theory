from constants import *


class TokenType:
    def __init__(self, name: str, regex: str):
        self.name = name
        self.regex = regex

    def __str__(self):
        return self.name

# TODO: Сделать не {SPACE}, а что-то типа "не буква"
TOKEN_TYPES = [
    TokenType('BLOCK_COMMENT', f'{{.*}}'),
    TokenType('LINE_COMMENT', f'//.*\n'),
    TokenType('ARRAY', f'(A|a)(R|r)(R|r)(A|a)(Y|y){SPACE}'),
    TokenType('BEGIN', f'(B|b)(E|e)(G|g)(I|i)(N|n){SPACE}'),
    TokenType('ELSE', f'(E|e)(L|l)(S|s)(E|e){SPACE}'),
    TokenType('END', f'(E|e)(N|n)(D|d){SPACE}'),
    TokenType('IF', f'(I|i)(F|f){SPACE}'),
    TokenType('OF', f'(O|o)(F|f){SPACE}'),
    TokenType('OR', f'(O|o)(R|r){SPACE}'),
    TokenType('PROGRAM', f'(P|p)(R|r)(O|o)(G|g)(R|r)(A|a)(M|m){SPACE}'),
    TokenType('PROCEDURE', f'(P|p)(R|r)(O|o)(C|c)(E|e)(D|d)(U|u)(R|r)(E|e){SPACE}'),
    TokenType('THEN', f'(T|t)(H|h)(E|e)(N|n){SPACE}'),
    TokenType('TYPE', f'(T|t)(Y|y)(P|p)(E|e){SPACE}'),
    TokenType('VAR', f'(V|v)(A|a)(R|r){SPACE}'),
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
    TokenType('DOT', '\\.'),
    TokenType('IDENTIFIER', f'({LETTER}|_)({LETTER_OR_DIGIT}|_)*'),
    TokenType('STRING', f'\'.*\''),
    TokenType('FLOAT', f'{NUMBER}\\.{DIGIT}+'),
    TokenType('INTEGER', NUMBER),
    TokenType('SPACE', SPACE),
]
