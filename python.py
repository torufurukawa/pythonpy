def main():
    code = "print()"
    tokens = tokeinze(code)
    ast = parse(tokens)
    evaluate(ast)


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
    print(file=fout)


class PrintNode:
    pass


if __name__ == "__main__":
    main()
