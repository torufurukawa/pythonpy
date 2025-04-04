def main(fin, fout):
    code = fin.getvalue()
    tokens = tokenize(code)
    ast = parse(tokens)
    evaluate(ast, fout)


def tokenize(code):
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

        elif c == "+":
            tokens.append(("PLUS", c))
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
    elif (tokens[0][0] == "PRINT" and
          tokens[1][0] == "LPAREN" and
          tokens[-1][0] == "RPAREN"):
        inner_tokens = tokens[2:-1]
        expr = parse_expr(inner_tokens)
        return PrintNode(expr)
    else:
        raise SyntaxError("Failed to parse")


def parse_atom(token):
    type_, value = token
    if type_ == "NUMBER":
        return int(value)
    else:
        raise SyntaxError("Expected a number")


def parse_expr(tokens):
    if (len(tokens) == 1) and (tokens[0][0] == "NUMBER"):
        return parse_atom(tokens[0])
    elif (len(tokens) == 3 and
          tokens[0][0] == "NUMBER" and
          tokens[1][0] == "PLUS" and
          tokens[2][0] == "NUMBER"):
        left = parse_atom(tokens[0])
        right = parse_atom(tokens[2])
        return BinOpNode(left, "+", right)
    else:
        raise SyntaxError("Unsupported expression")


def evaluate(node, fout):
    if isinstance(node, PrintNode):
        if node.value is None:
            print(file=fout)
        else:
            print(node.value, file=fout)
    else:
        raise TypeError("Unknown node type")


def evaluate_expr(expr):
    if isinstance(expr, int):
        return expr
    elif isinstance(expr, BinOpNode):
        left = evaluate_expr(expr.left)
        right = evaluate_expr(expr.right)
        if expr.op == "+":
            return left + right
        else:
            raise ValueError(f"Unknown operator: {expr.op}")


class PrintNode:
    def __init__(self, value=None):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, PrintNode) and self.value == other.value

    def __repr__(self):
        return f"PrintNode({self.value})"


class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __eq__(self, other):
        return (
            isinstance(other, BinOpNode) and
            self.left == other.left and
            self.op == other.op and
            self.right == other.right
        )

    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op}, {self.right})"
