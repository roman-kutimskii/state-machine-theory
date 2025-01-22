from lexer_token import LexerToken
from simulator import Simulator
from token_type import TOKEN_TYPES

SIMULATORS_MAP = {token.name: Simulator(token.regex) for token in TOKEN_TYPES}


class Lexer:
    def __init__(self, input_file: str):
        self.file = open(input_file, 'r', encoding='utf-8')
        self.buffer = ''
        self.line = 1
        self.column = 1
        self.eof = False

    def _fill_buffer(self) -> None:
        if not self.eof:
            chunk = self.file.read(1024)
            if chunk:
                self.buffer += chunk
                if not any(map(lambda space: space in self.buffer, ' \n\t\r')):
                    self._fill_buffer()
                if '//' in self.buffer and '\n' not in self.buffer:
                    self._fill_buffer()
                if '{' in self.buffer and '}' not in self.buffer:
                    self._fill_buffer()
            else:
                self.eof = True

    def next_token(self) -> LexerToken | None:
        while not self.eof or self.buffer:
            self._fill_buffer()
            if not self.buffer:
                return None

            for token_type in TOKEN_TYPES:
                token_name = token_type.name
                simulator = SIMULATORS_MAP.get(token_type.name)
                result = simulator.run(self.buffer)
                if result:
                    if token_name in (
                    'LINE_COMMENT', 'ARRAY', 'BEGIN', 'ELSE', 'END', 'IF', 'OF', 'OR', 'PROGRAM', 'PROCEDURE', 'THEN',
                    'TYPE', 'VAR', 'IDENTIFIER', 'BAD'):
                        result = result[:-1]
                    if token_name == "INTEGER":
                        if len(result) > 16:
                            token_name = "BAD"
                    if token_name == "IDENTIFIER":
                        if len(result) > 256:
                            token_name = "BAD"
                    if token_name in ('BAD_IDENTIFIER', 'BAD_STRING'):
                        token_name = "BAD"
                    token = LexerToken(token_name, result, (self.line, self.column))
                    self._update_position(result)
                    return token

            bad_char = self.buffer[0]
            self.buffer = self.buffer[1:]
            self.column += 1
            return LexerToken('BAD', bad_char, (self.line, self.column - 1))

        return None

    def _update_position(self, result: str) -> None:
        self.buffer = self.buffer[len(result):]
        self.column += len(result)
        if '\n' in result:
            lines = result.split('\n')
            self.line += len(lines) - 1
            self.column = len(lines[-1]) + 1

    def close(self) -> None:
        if self.file is not None:
            self.file.close()
            self.file = None
