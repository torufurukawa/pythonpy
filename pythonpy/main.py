from .lexer import tokenize
from .parser import parse
from .evaluator import evaluate


def main(fin, fout):
    code = fin.getvalue()
    tokens = tokenize(code)
    ast = parse(tokens)
    evaluate(ast, fout)
