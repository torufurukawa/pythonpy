from .nodes import PrintNode, BinOpNode


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

    node, i = parse_term(tokens, 0)
    while i < len(tokens):
        if tokens[i].type not in ("PLUS", "MINUS"):
            raise SyntaxError(f"Unexpected token: {tokens[i]}")

        op = tokens[i].value
        right, i = parse_term(tokens, i+1)
        node = BinOpNode(node, op, right)

    return node


def parse_factor(tokens, i):
    if len(tokens) <= i:
        raise SyntaxError("Expected number")

    token = tokens[i]
    if token.type != "NUMBER":
        raise SyntaxError(f"Unexpected token in factor: {token}")

    return int(token.value), i+1


def parse_term(tokens, i):
    node, i = parse_factor(tokens, i)

    while i < len(tokens) and tokens[i].type in ["MULTIPLY", "DIVIDE"]:
        op = tokens[i].value
        right, i = parse_factor(tokens, i + 1)
        node = BinOpNode(node, op, right)

    return node, i
