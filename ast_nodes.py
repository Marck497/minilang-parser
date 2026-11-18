class NumberNode:
    def __init__(self, value):
        self.value = value


class VarNode:
    def __init__(self, name):
        self.name = name


class BinaryOpNode:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryOpNode:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class AssignNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class PrintNode:
    def __init__(self, expr):
        self.expr = expr


class IfNode:
    def __init__(self, cond, then_branch, else_branch=None):
        self.cond = cond
        self.then_branch = then_branch
        self.else_branch = else_branch


def show(node, indent=0):
    """Print the tree, one node per line, indented by depth."""
    pad = "    " * indent

    if isinstance(node, list):
        for item in node:
            show(item, indent)

    elif isinstance(node, NumberNode):
        print(pad + "Number", node.value)

    elif isinstance(node, VarNode):
        print(pad + "Variable", node.name)

    elif isinstance(node, BinaryOpNode):
        print(pad + "BinaryOp", node.op)
        show(node.left, indent + 1)
        show(node.right, indent + 1)

    elif isinstance(node, UnaryOpNode):
        print(pad + "UnaryOp", node.op)
        show(node.expr, indent + 1)

    elif isinstance(node, AssignNode):
        print(pad + "Assign", node.name)
        show(node.expr, indent + 1)

    elif isinstance(node, PrintNode):
        print(pad + "Print")
        show(node.expr, indent + 1)

    elif isinstance(node, IfNode):
        print(pad + "If")
        show(node.cond, indent + 1)

        print(pad + "Then")
        show(node.then_branch, indent + 1)

        if node.else_branch is not None:
            print(pad + "Else")
            show(node.else_branch, indent + 1)
