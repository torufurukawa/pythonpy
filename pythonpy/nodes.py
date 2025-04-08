class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode({len(self.statements)} statements)"


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


class AssignNode:
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

    def __eq__(self, other):
        return (
            isinstance(other, AssignNode) and
            self.var_name == other.var_name and
            self.expr == other.expr
        )

    def __expr__(self):
        return f"AssignNode({self.var_name} = {self.expr})"
