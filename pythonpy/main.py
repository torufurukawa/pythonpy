from .lexer import tokenize_program
from .parser import parse_program
from .evaluator import evaluate


def main(fin, fout):
    code = fin.getvalue()
    token_lines = tokenize_program(code)
    program_node = parse_program(token_lines)
    evaluate(program_node, fout)
