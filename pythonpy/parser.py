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
        expr = parse_expr_wrapper(inner_tokens)
        return PrintNode(expr)
    else:
        raise SyntaxError("Failed to parse")


def parse_atom(token):
    if token.type == "NUMBER":
        return int(token.value)
    else:
        raise SyntaxError("Expected a number")


def parse_expr_wrapper(tokens):
    node, i = parse_expr(tokens, 0)
    return node


def parse_expr(tokens, index):
    if not tokens:
        raise SyntaxError("Empty expression")

    node, i = parse_term(tokens, index)
    while i < len(tokens):
        if tokens[i].type not in ("PLUS", "MINUS"):
            raise SyntaxError(f"Unexpected token: {tokens[i]}")

        op = tokens[i].value
        right, i = parse_term(tokens, i+1)
        node = BinOpNode(node, op, right)

    return node, i


def parse_factor(tokens, i):
    if len(tokens) <= i:
        raise SyntaxError("Expected number or '('")

    token = tokens[i]

    if token.type == "NUMBER":
        return int(token.value), i+1

    # elif token.type == "LPAREN":
    #     expr, next_i = parse_expr(tokens, i+1)
    #     if len(tokens) <= next_i or tokens[next_i].type != "RPAREN":
    #         raise SyntaxError("Expected ')'")
    #     return expr, next_i + 1

    raise SyntaxError(f"Unexpected token in factor: {token}")


def parse_term(tokens, i):
    node, i = parse_factor(tokens, i)

    while i < len(tokens) and tokens[i].type in ["MULTIPLY", "DIVIDE"]:
        op = tokens[i].value
        right, i = parse_factor(tokens, i + 1)
        node = BinOpNode(node, op, right)

    return node, i
