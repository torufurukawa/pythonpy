def main(fin, fout):
    code = fin.getvalue()
    tokens = tokeinze(code)
    ast = parse(tokens)
    evaluate(ast, fout)


def tokeinze(code):
    tokens = []
    i = 0

    while i < len(code):
        c = code[i]

        if c in ' \t\n':
            i += 1

        elif code[i:].startswith("print", i):
            tokens.append(("PRINT", "print"))
            i += 5

        elif c == "(":
            tokens.append(("LPAREN", c))
            i += 1

        elif c == ")":
            tokens.append(("RPAREN", c))
            i += 1

        elif c.isdigit():
            start = i
            while i < len(code) and code[i].isdigit():
                i += 1
            number = code[start:i]
            tokens.append(("NUMBER", number))

        else:
            raise SyntaxError(f"Unexpected character: '{c}' at position {i}")

    return tokens


def parse(tokens):
    if tokens == [("PRINT", "print"), ("LPAREN", "("), ("RPAREN", ")")]:
        return PrintNode()
    elif (len(tokens) == 4 and
          [type_ for type_, _ in tokens] == ["PRINT", "LPAREN", "NUMBER",
                                             "RPAREN"]):
        return PrintNode(int(tokens[2][1]))
    else:
        raise SyntaxError("Failed to parse")


def evaluate(node, fout):
    if isinstance(node, PrintNode):
        if node.value is None:
            print(file=fout)
        else:
            print(node.value, file=fout)
    else:
        raise TypeError("Unknown node type")


class PrintNode:
    def __init__(self, value=None):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, PrintNode) and self.value == other.value
