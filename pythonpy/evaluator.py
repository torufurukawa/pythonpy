from .nodes import ProgramNode, PrintNode, BinOpNode, AssignNode


def evaluate(node, env, fout):
    if isinstance(node, ProgramNode):
        for statement in node.statements:
            evaluate(statement, env, fout)

    elif isinstance(node, PrintNode):
        if node.value is None:
            print(file=fout)
        else:
            result = evaluate_expr(node.value)
            print(result, file=fout)

    elif isinstance(node, AssignNode):
        env[node.var_name] = evaluate_expr(node.expr)

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
        elif expr.op == "-":
            return left - right
        elif expr.op == "*":
            return left * right
        elif expr.op == "/":
            if right == 0:
                raise ValueError("Division by zero")
            return left // right
        else:
            raise ValueError(f"Unknown operator: {expr.op}")
    else:
        raise TypeError("Unsupported expression node")
