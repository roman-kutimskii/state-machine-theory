import sys

from lexer import Lexer
from lexer_token import LexerToken


def main() -> int:
    if len(sys.argv) not in {3, 4}:
        print(f'Usage: python {sys.argv[0]} <input-file> <output-file> [debug]')
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    debug = sys.argv[3] == 'debug' if len(sys.argv) == 4 else False

    lexer = Lexer(input_file)

    with open(output_file, 'w', encoding='utf-8') as output:
        bad_collector = LexerToken('BAD', '', (0, 0))
        while True:
            token = lexer.next_token()
            if token is None:
                break
            if token.type == 'BAD':
                bad_collector.value += token.value
                if not bad_collector.pos[0] and not bad_collector.pos[1]:
                    bad_collector.pos = token.pos
                continue
            if bad_collector.value:
                print(bad_collector) if debug else None
                output.write(str(bad_collector) + '\n')
                bad_collector.value = ''
                bad_collector.pos = (0, 0)
            if token.type not in ('SPACE', 'LINE_COMMENT', 'BLOCK_COMMENT'):
                print(token) if debug else None
                output.write(str(token) + '\n')
        if bad_collector.value:
            print(bad_collector) if debug else None
            output.write(str(bad_collector) + '\n')

    lexer.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())
