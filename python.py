from dataclasses import dataclass


def main(fin, fout):
    code = fin.getvalue()
    tokens = tokenize(code)
    ast = parse(tokens)
    evaluate(ast, fout)


@dataclass
class Token:
    type: str
    value: str


def tokenize(code):
    tokens = []
    i = 0

    while i < len(code):
        c = code[i]

        if c in " \t\n":
            i += 1

        elif code[i:].startswith("print", i):
            tokens.append(Token("PRINT", "print"))
            i += 5

        elif c == "(":
            tokens.append(Token("LPAREN", c))
            i += 1

        elif c == ")":
            tokens.append(Token("RPAREN", c))
            i += 1

        elif c == "+":
            tokens.append(Token("PLUS", c))
            i += 1

        elif c.isdigit():
            start = i
            while i < len(code) and code[i].isdigit():
                i += 1
            number = code[start:i]
            tokens.append(Token("NUMBER", number))

        else:
            raise SyntaxError(f"Unexpected character: '{c}' at position {i}")

    return tokens


def parse(tokens):
    if (
        len(tokens) == 3
        and tokens[0].type == "PRINT"
        and tokens[1].type == "LPAREN"
        and tokens[2].type == "RPAREN"
    ):
        return PrintNode()
    elif (
        tokens[0].type == "PRINT"
        and tokens[1].type == "LPAREN"
        and tokens[-1].type == "RPAREN"
    ):
        inner_tokens = tokens[2:-1]
        expr = parse_expr(inner_tokens)
        return PrintNode(expr)
    else:
        raise SyntaxError("Failed to parse")


def parse_atom(token):
    if token.type == "NUMBER":
        return int(token.value)
    else:
        raise SyntaxError("Expected a number")


def parse_expr(tokens):
    if not tokens:
        raise SyntaxError("Empty expression")

    left = parse_atom(tokens[0])
    i = 1

    while i < len(tokens):
        if tokens[i].type == "PLUS":
            if len(tokens) <= i + 1:
                raise SyntaxError("Expected right-hand operand after '+'")

            op = tokens[i].value
            right = parse_atom(tokens[i + 1])
            left = BinOpNode(left, op, right)
            i += 2
        else:
            raise SyntaxError(f"Unexpected token: {tokens[i]}")

    return left

    if (len(tokens) == 1) and (tokens[0].type == "NUMBER"):
        return parse_atom(tokens[0])
    elif (
        len(tokens) == 3
        and tokens[0].type == "NUMBER"
        and tokens[1].type == "PLUS"
        and tokens[2].type == "NUMBER"
    ):
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
            result = evaluate_expr(node.value)
            print(result, file=fout)
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
    else:
        raise TypeError("Unsupported expression node")


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
            isinstance(other, BinOpNode)
            and self.left == other.left
            and self.op == other.op
            and self.right == other.right
        )

    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op}, {self.right})"
