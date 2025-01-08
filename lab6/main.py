import sys

from lexer import Lexer


def main():
    if len(sys.argv) != 3:
        print(f'Usage: python {sys.argv[0]} <input-file> <output-file>')
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    lexer = Lexer(input_file)

    with open(output_file, 'w', encoding='utf-8') as output:
        while True:
            token = lexer.next_token()
            if token is None:
                break
            print(token)
            output.write(str(token) + '\n')

    lexer.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())
