import sys

from lexer import Lexer


def process(input_file_name, output_file_name):
    with open(input_file_name, 'r') as input_file:
        text = input_file.readlines()
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    with open(output_file_name, 'w') as output_file:
        for token in tokens:
            output_file.write(str(token))


def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <input-file> <output-file>')
        return 1

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    try:
        process(input_file_name, output_file_name)
    except RuntimeError as e:
        print(e)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
