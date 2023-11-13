import pytest
from interpreter import Interpreter, BinOp, UnOp, Number, NodeVisitor, Variable, Empty, Semi, Assigment
from interpreter import Token, TokenType, Parser


@pytest.fixture(scope="function")
def interpreter():
    return Interpreter()


@pytest.fixture(scope="function")
def parser():
    return Parser()


class TestInterpreter:
    interpreter = Interpreter()

    def test_empty(self, interpreter):
        assert interpreter.eval("BEGIN END.") == {}

    def test_variable(self, interpreter):
        assert interpreter.eval("BEGIN x:= 2 + 3 * (2 + 3); END.") == {'x': 17.0}

    def test_NodeVisitor(self):
        assert NodeVisitor().visit() is None

    def test_uninitialized_variable(self, interpreter):
        with pytest.raises(ValueError):
            interpreter.eval("BEGIN b := -10 + +a + 10 * y / 4; END.")

    def test_bad_token(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_ASSIGN(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a== 2 + 3 * (2 + 3); END.")


