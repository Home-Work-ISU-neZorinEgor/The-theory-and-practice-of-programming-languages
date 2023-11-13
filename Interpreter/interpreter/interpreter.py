from typing import Any

from .parser import Parser
from .ast import BinOp, Number, UnOp, Var, Empty, Semi, Assigment


class NodeVisitor:

    def visit(self):
        return


class Interpreter(NodeVisitor):

    variable: dict[Any, Any]

    def __init__(self):
        self.parser = Parser()
        self.variable = {}

    def visit(self, node):
        match node:
            case Number():
                return self.visit_num(node)
            case BinOp():
                return self.visit_binop(node)
            case UnOp():
                return self.visit_unop(node)
            case Var():
                return self.visit_var(node)
            case Empty():
                return self.visit_empty()
            case Semi():
                return self.visit_semi(node)
            case Assigment():
                return self.visit_assigment(node)

    def visit_num(self, node):
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

    def visit_var(self, node):
        if node.token.value not in list(self.variable.keys()):
            raise ValueError("Uninitialized variable")
        return self.variable[node.token.value]

    def visit_empty(self):
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
        self.visit(tree)
        return self.variable
