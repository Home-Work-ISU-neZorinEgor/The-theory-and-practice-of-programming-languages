from .parser import Parser
from .ast import Number, BinOp, UnOp, Variable

class NodeVisitor:

    def visit(self):
        return

class Interpreter(NodeVisitor):

    def __init__(self):
        self.parser = Parser()

    def visit(self, node):
        if isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, BinOp):
            return self.visit_binop(node)
        elif isinstance(node, UnOp):
            return self.visit_unop(node)

        elif isinstance(node, Variable):
            return self.visit_variable(node)
        elif isinstance(node, Empty):
            return self.visit_empty(node)
        elif isinstance(node, Semi):
            return self.visit_semi(node)
        elif isinstance(node, Assigment):
            return self.visit_assigment(node)

    def visit_number(self, node):
        return float(node.token.value)

    def visit_binop(self, node):
        match node.op.value:
            case "+":
                return self.visit(node.left) + self.visit(node.right)
            case "-":
                return self.visit(node.left) - self.visit(node.right)
            case "*":
                return self.visit(node.left) * self.visit(node.right)
            case "/":
                return self.visit(node.left) / self.visit(node.right)
            case _:
                raise ValueError("Invalid operator")

    def visit_unop(self, node):
        match node.op.value:
            case "+":
                return self.visit(node.right)
            case "-":
                return self.visit(node.right) * -1
            case _:
                raise ValueError("Invalid operator")

    def visit_variable(self, node):
        if node.token.value not in list(self.variable.keys()):
            raise ValueError("Uninitialized variable")
        return self.variable[node.token.value]

    def visit_empty(self, node):
        return ""


    def visit_semi(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_assigment(self, node):
        if node.variable.value not in list(self.variable.keys()):
            self.variable[node.variable.value] = 0
        self.variable[node.variable.value] = self.visit(node.right)

    def eval(self, code):
        tree = self.parser.parse(code)
        return self.visit(tree)
