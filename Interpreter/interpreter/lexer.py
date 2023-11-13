from .token import Token, TokenType

class Lexer():

    def __init__(self):
        self._pos = 0
        self._text = ""
        self._current_char = None

    def init(self, text):
        self._text = text
        self._pos = 0
        self._current_char = self._text[self._pos]

    def forward(self):
        self._pos += 1
        if self._pos > len(self._text) - 1:
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def skip(self):
        while (self._current_char is not None and
               self._current_char.isspace()):
            self.forward()

    def message(self):
        result = []
        while (self._current_char is not None and self._current_char not in [";", ":", " ", "=", "."]):
            result.append(self._current_char)
            self.forward()
        return "".join(result)

    def asing(self):
        while self._current_char:
            if self._current_char.isspace():
                self.skip()
                continue
            if self._current_char[0] == "=":
                self.forward()
                return ":="
            raise SyntaxError("bad token")

    def number(self):
        result  = []
        while (self._current_char is not None and
               (self._current_char.isdigit() or
                self._current_char == ".")):
            result.append(self._current_char)
            self.forward()
        return "".join(result)

    def next(self):
        while self._current_char:
            if self._current_char.isspace():
                self.skip()
                continue
            if self._current_char.isdigit():
                return Token(TokenType.NUMBER, self.number())
            if self._current_char in ["+", "-", "/", "*"]:
                op = self._current_char
                self.forward()
                return Token(TokenType.OPERATOR, op)
            if self._current_char == "(":
                op = self._current_char
                self.forward()
                return Token(TokenType.LPAREN, op)
            if self._current_char == ")":
                op = self._current_char
                self.forward()
                return Token(TokenType.RPAREN, op)

            if self._current_char == ";":
                semi = self._current_char
                self.forward()
                return Token(TokenType.SEMI, semi)
            if self._current_char == ":":
                self.forward()
                return Token(TokenType.ASSIGN, self.asing())
            if self._current_char == ".":
                dot = self._current_char
                return Token(TokenType.DOT, dot)

            mes = self.message()
            if mes == "BEGIN":
                return Token(TokenType.BEGIN, mes)
            if mes == "END":
                return Token(TokenType.END, mes)
            if mes != "":
                return Token(TokenType.ID, mes)

            raise SyntaxError("bad token")
