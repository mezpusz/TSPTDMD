from input import parse_input
import sys

if len(sys.argv) < 2:
    print('Filename should be given as first parameter!')
    exit(-1)

print(parse_input(sys.argv[1]))
