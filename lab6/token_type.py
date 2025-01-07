from constants import *


class TokenType:
    def __init__(self, name: str, regex: str):
        self.name = name
        self.regex = regex

    def __repr__(self):
        return self.name


token_types_map = {
    'ARRAY': TokenType('ARRAY', '(A|a)(R|r)(R|r)(A|a)(Y|y)'),
    'BEGIN': TokenType('BEGIN', '(B|b)(E|e)(G|g)(I|i)(N|n)'),
    'ELSE': TokenType('ELSE', '(E|e)(L|l)(S|s)(E|e)'),
    'END': TokenType('END', '(E|e)(N|n)(D|d)'),
    'IF': TokenType('IF', '(I|i)(F|f)'),
    'OF': TokenType('OF', '(O|o)(F|f)'),
    'OR': TokenType('OR', '(O|o)(R|r)'),
    'PROGRAM': TokenType('PROGRAM', '(P|p)(R|r)(O|o)(G|g)(R|r)(A|a)(M|m)'),
    'PROCEDURE': TokenType('PROCEDURE', '(P|p)(R|r)(O|o)(C|c)(E|e)(D|d)(U|u)(R|r)(E|e)'),
    'THEN': TokenType('THEN', '(T|t)(H|h)(E|e)(N|n)'),
    'TYPE': TokenType('TYPE', '(T|t)(Y|y)(P|p)(E|e)'),
    'VAR': TokenType('VAR', '(V|v)(A|a)(R|r)'),
    'MULTIPLICATION': TokenType('MULTIPLICATION', '\\*'),
    'PLUS': TokenType('PLUS', '\\+'),
    'MINUS': TokenType('MINUS', '-'),
    'DIVIDE': TokenType('DIVIDE', '/'),
    'SEMICOLON': TokenType('SEMICOLON', ';'),
    'COMMA': TokenType('COMMA', ','),
    'LEFT_PAREN': TokenType('LEFT_PAREN', '\\('),
    'RIGHT_PAREN': TokenType('RIGHT_PAREN', '\\)'),
    'LEFT_BRACKET': TokenType('LEFT_BRACKET', '['),
    'RIGHT_BRACKET': TokenType('RIGHT_BRACKET', ']'),
    'EQ': TokenType('EQ', '='),
    'GREATER': TokenType('GREATER', '>'),
    'LESS': TokenType('LESS', '<'),
    'LESS_EQ': TokenType('LESS_EQ', '<='),
    'GREATER_EQ': TokenType('GREATER_EQ', '>='),
    'NOT_EQ': TokenType('NOT_EQ', '<>'),
    'COLON': TokenType('COLON', ':'),
    'ASSIGN': TokenType('ASSIGN', ':='),
    'DOT': TokenType('DOT', '.'),
    'IDENTIFIER': TokenType('IDENTIFIER', f'{LETTER}|_({SYMBOL}|_)*'),
    'STRING': TokenType('STRING', f'\'{SYMBOL}*\''),
    'INTEGER': TokenType('INTEGER', f'(ε|-){NUMBER}'),
    'FLOAT': TokenType('FLOAT', f'(ε|-){NUMBER}.{DIGIT}+'),
    'LINE_COMMENT': TokenType('LINE_COMMENT', f'//{SYMBOL}*\n'),
    'BLOCK_COMMENT': TokenType('BLOCK_COMMENT', f'{{{SYMBOL}*}}'),
    'SPACE': TokenType('SPACE', f' |\\n|\\t|\\r'),
    'BAD': TokenType('BAD', f'{SYMBOL}*'),
}
