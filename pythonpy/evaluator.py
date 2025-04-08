from .nodes import ProgramNode, PrintNode, BinOpNode, AssignNode, NameNode


def evaluate(node, env, fout):
    if isinstance(node, ProgramNode):
        for statement in node.statements:
            evaluate(statement, env, fout)

    elif isinstance(node, PrintNode):
        if node.value is None:
            print(file=fout)
        else:
            result = evaluate_expr(node.value, env)
            print(result, file=fout)

    elif isinstance(node, AssignNode):
        env[node.var_name] = evaluate_expr(node.expr, env)

    else:
        raise TypeError("Unknown node type")


def evaluate_expr(expr, env):
    if isinstance(expr, int):
        return expr

    elif isinstance(expr, BinOpNode):
        left = evaluate_expr(expr.left, env)
        right = evaluate_expr(expr.right, env)
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

    elif isinstance(expr, NameNode):
        if expr.var_name not in env:
            raise NameError(f"Undefined variable: {expr.var_name}")
        return env[expr.var_name]

    else:
        raise TypeError("Unsupported expression node")
