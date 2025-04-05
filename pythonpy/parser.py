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

    left = parse_atom(tokens[0])
    i = 1

    while i < len(tokens):
        if tokens[i].type in ["PLUS", "MINUS"]:
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
