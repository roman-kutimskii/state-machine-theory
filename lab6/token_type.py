from constants import *


class TokenType:
    def __init__(self, name: str, regex: str):
        self.name = name
        self.regex = regex


token_types_list = {
    'ARRAY': TokenType('ARRAY', '(A|a)(R|r)(R|r)(A|a)(Y|y)'),
    'BEGIN': TokenType('BEGIN', 'BEGIN'),
    'ELSE': TokenType('ELSE', 'ELSE'),
    'END': TokenType('END', 'END'),
    'IF': TokenType('IF', 'IF'),
    'OF': TokenType('OF', 'OF'),
    'OR': TokenType('OR', 'OR'),
    'PROGRAM': TokenType('PROGRAM', 'PROGRAM'),
    'PROCEDURE': TokenType('PROCEDURE', 'PROCEDURE'),
    'THEN': TokenType('THEN', 'THEN'),
    'TYPE': TokenType('TYPE', 'TYPE'),
    'VAR': TokenType('VAR', 'VAR'),
    'MULTIPLICATION': TokenType('MULTIPLICATION', '\*'),
    'PLUS': TokenType('PLUS', '\+'),
    'MINUS': TokenType('MINUS', '-'),
    'DIVIDE': TokenType('DIVIDE', '/'),
    'SEMICOLON': TokenType('SEMICOLON', ';'),
    'COMMA': TokenType('COMMA', ','),
    'LEFT_PAREN': TokenType('LEFT_PAREN', '\('),
    'RIGHT_PAREN': TokenType('RIGHT_PAREN', '\)'),
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
    'BAD': TokenType('BAD', f'{SYMBOL}*'),
    'SPACE': TokenType('SPACE', f' |\\n|\\t|\\r'),
}
