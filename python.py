def main(fin, fout):
    code = fin.getvalue()
    tokens = tokeinze(code)
    ast = parse(tokens)
    evaluate(ast, fout)


def tokeinze(code):
    code = code.strip()
    if code == "print()":
        return [("PRINT", "print"), ("LPAREN", "("), ("RPAREN", ")")]
    else:
        raise SyntaxError("Unsupported statement")


def parse(tokens):
    if tokens == [("PRINT", "print"), ("LPAREN", "("), ("RPAREN", ")")]:
        return PrintNode()
    else:
        raise SyntaxError("Failed to parse")


def evaluate(node, fout):
    if isinstance(node, PrintNode):
        print(file=fout)
    else:
        raise TypeError("Unknown node type")


class PrintNode:
    pass
