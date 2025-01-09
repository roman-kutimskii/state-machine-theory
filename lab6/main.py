import sys

from lexer import Lexer


def main() -> int:
    if len(sys.argv) not in {3, 4}:
        print(f'Usage: python {sys.argv[0]} <input-file> <output-file> [debug]')
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    debug = sys.argv[3] == 'debug' if len(sys.argv) == 4 else False

    lexer = Lexer(input_file)

    with open(output_file, 'w', encoding='utf-8') as output:
        while True:
            token = lexer.next_token()
            if token is None:
                break
            if token.type != 'SPACE':
                print(token) if debug else None
                output.write(str(token) + '\n')

    lexer.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())
