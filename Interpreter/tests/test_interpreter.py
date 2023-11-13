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

    def test_bad_token_SEMI(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_DOT(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_END(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_ID(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_LPAREN(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")

    def test_bad_token_RPAREN(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a= 2 + 3 * (2 + 3); END.")


    def test_invalid_token_order(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a = 2 + 3 * (2 + 3); END.")

    def test_Invalid_statement(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a = 2 + 3 * (2 + 3); END.")

    def test_Invalid_statement_assign(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN a = 2 + 3 * (2 + 3); END.")

    def test_ast_Assigment_num(self):
        assert Assigment(Variable(Token(TokenType.ID, "h")), Number(Token(TokenType.NUMBER, "2"))).__str__() == \
               f"Assigment Variable (Token(TokenType.ID, h)) (Number (Token(TokenType.NUMBER, 2)))"

    def test_ast_Assigment_str(self):
        assert Assigment(Variable(Token(TokenType.ID, "h")), Number(Token(TokenType.NUMBER, "2"))).__str__() == \
               f"Assigment Variable (Token(TokenType.ID, h)) (Number (Token(TokenType.NUMBER, 2)))"

    def test_ast_Empty(self):
        assert Empty(Token(TokenType.END, "END.")).__str__() == "Empty (Token(TokenType.END, END.))"

    def test_ast_BinOp_str(self):
        assert BinOp(Number(Token(TokenType.NUMBER, "2")), Token(TokenType.OPERATOR, "+"),
                     Number(Token(TokenType.NUMBER, "2"))).__str__() == \
               f"BinOp+ (Number (Token(TokenType.NUMBER, 2)), Number (Token(TokenType.NUMBER, 2)))"

    def test_BinOp_invalid_operator(self, interpreter):
        with pytest.raises(ValueError):
            interpreter.visit_binop(BinOp(Number(Token(TokenType.NUMBER, "2")), Token(TokenType.OPERATOR, "&"),
                                          Number(Token(TokenType.NUMBER, "2"))))

    def test_unop_invalid_operator(self, interpreter):
        with pytest.raises(ValueError):
            interpreter.visit_unop(UnOp(Token(TokenType.OPERATOR, "&"), Number(Token(TokenType.NUMBER, "2"))))

    def test_ast_UnOp_str(self):
        assert UnOp(Token(TokenType.OPERATOR, "+"), Number(Token(TokenType.NUMBER, "2"))).__str__() == \
               f"UnOp+ (Number (Token(TokenType.NUMBER, 2)))"

    def test_ast_Number_str(self):
        assert Number(Token(TokenType.NUMBER, "2")).__str__() == "Number (Token(TokenType.NUMBER, 2))"

    def test_ast_Variable_str(self):
        assert Variable(Token(TokenType.ID, "h")).__str__() == "Variable (Token(TokenType.ID, h))"

    def test_ast_Assigment_str(self):
        assert Assigment(Variable(Token(TokenType.ID, "h")), Number(Token(TokenType.NUMBER, "2"))).__str__() == \
               f"Assigment Variable (Token(TokenType.ID, h)) (Number (Token(TokenType.NUMBER, 2)))"


