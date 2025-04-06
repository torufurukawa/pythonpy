from .lexer import tokenize_line
from .parser import parse
from .evaluator import evaluate


def main(fin, fout):
    code = fin.getvalue()
    tokens = tokenize_line(code)
    ast = parse(tokens)
    evaluate(ast, fout)
