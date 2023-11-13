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
        match self._pos > len(self._text) - 1:
            case True:
                self._current_char = None
            case False:
                self._current_char = self._text[self._pos]

    def skip(self):
        while (self._current_char is not None and
               self._current_char.isspace()):
            self.forward()

    def number(self):
        result = []
        while (self._current_char is not None and
               (self._current_char.isdigit() or
                self._current_char == ".")):
            result.append(self._current_char)
            self.forward()
        return "".join(result)

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

            match self._current_char[0]:
                case "=":
                    self.forward()
                    return ":="

            raise SyntaxError("bad token")

    def next(self):
        while self._current_char:
            if self._current_char.isspace():
                self.skip()
                continue

            match self._current_char:
                case char if char.isdigit():
                    return Token(TokenType.NUMBER, self.number())
                case char if char in ["+", "-", "/", "*"]:
                    op = char
                    self.forward()
                    return Token(TokenType.OPERATOR, op)
                case "(":
                    op = self._current_char
                    self.forward()
                    return Token(TokenType.LPAREN, op)
                case ")":
                    op = self._current_char
                    self.forward()
                    return Token(TokenType.RPAREN, op)
                case ";":
                    semi = self._current_char
                    self.forward()
                    return Token(TokenType.SEMI, semi)
                case ":":
                    self.forward()
                    return Token(TokenType.ASSIGN, self.asing())
                case ".":
                    dot = self._current_char
                    return Token(TokenType.DOT, dot)

            mes = self.message()
            match mes:
                case "BEGIN":
                    return Token(TokenType.BEGIN, mes)
                case "END":
                    return Token(TokenType.END, mes)
                case _ if mes != "":
                    return Token(TokenType.ID, mes)

            raise SyntaxError("bad token")
