from loxtoken import Token
from loxtokentype import TokenType as TT
from errors import error

_keywords: dict[str, TT] = {
    'and': TT.AND,
    'class': TT.CLASS,
    'else': TT.ELSE,
    'false': TT.FALSE,
    'for': TT.FOR,
    'fun': TT.FUN,
    'if': TT.IF,
    'nil': TT.NIL,
    'or': TT.OR,
    'print': TT.PRINT,
    'return': TT.RETURN,
    'super': TT.SUPER,
    'this': TT.THIS,
    'true': TT.TRUE,
    'var': TT.VAR,
    'while': TT.WHILE,
}


class Scanner:

    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []

        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def scanTokens(self) -> list[Token]:
        while not self.isAtEnd():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TT.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self) -> None:
        c = self.advance()
        match c:
            case '(':
                self.addToken(TT.LEFT_PAREN)
            case ')':
                self.addToken(TT.RIGHT_PAREN)
            case '{':
                self.addToken(TT.LEFT_BRACE)
            case '}':
                self.addToken(TT.RIGHT_BRACE)
            case ',':
                self.addToken(TT.COMMA)
            case '.':
                self.addToken(TT.DOT)
            case '-':
                self.addToken(TT.MINUS)
            case '+':
                self.addToken(TT.PLUS)
            case ';':
                self.addToken(TT.SEMICOLON)
            case '*':
                self.addToken(TT.STAR)
            case '!':
                self.addToken(TT.BANG_EQUAL if self.match('=') else TT.BANG)
            case '=':
                self.addToken(TT.EQUAL_EQUAL if self.match('=') else TT.EQUAL)
            case '<':
                self.addToken(TT.LESS_EQUAL if self.match('=') else TT.LESS)
            case '>':
                self.addToken(TT.GREATER_EQUAL if self.match('=') else TT.GREATER)
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.isAtEnd():
                        self.advance()
                elif self.match('*'):
                    self.multilineComment()
                else:
                    self.addToken(TT.SLASH)
            case ' ' | '\r' | '\t':
                pass  # skip whitespace characters
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case c if self.isDigit(c):
                self.number()
            case c if self.isAlpha(c):
                self.identifier()
            case _:
                error(self.line, "Unexpected character.")

    def multilineComment(self) -> None:
        opening = 1  # unmatched comment openings

        while opening > 0:
            if self.isAtEnd():
                error(self.line, "Unterminated comment.")
                return
            elif self.isAtMultilineCommentStart():
                opening = opening + 1
                self.advance(by=2)
            elif self.isAtMultilineCommentEnd():
                opening = opening - 1
                self.advance(by=2)
            elif self.peek() == '\n':
                self.line += 1
                self.advance()
            else:
                self.advance()

    def identifier(self) -> None:
        global _keywords
        while self.isAlphaNumeric(self.peek()):
            self.advance()

        text = self.source[self.start: self.current]
        type = _keywords.get(text)

        if type is None:
            type = TT.IDENTIFIER

        self.addToken(type)

    def number(self) -> None:
        while self.isDigit(self.peek()):
            self.advance()

        # look for fractional part
        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()

            # consume the "."
            while self.isDigit(self.peek()):
                self.advance()

        value = float(self.source[self.start: self.current])
        self.addToken(TT.NUMBER, literal=value)

    def string(self) -> None:
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.line = self.line + 1
            self.advance()

        if self.isAtEnd():
            error(self.line, "Unterminated string.")
            return

        self.advance()

        value = self.source[self.start + 1: self.current - 1]
        self.addToken(TT.STRING, literal=value)

    def match(self, expected: str) -> bool:
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False

        self.current = self.current + 1
        return True

    def peek(self) -> str:
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    def peekNext(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def isAtMultilineCommentStart(self) -> bool:
        return (self.peek() == '/' and self.peekNext() == '*')

    def isAtMultilineCommentEnd(self) -> bool:
        return (self.peek() == '*' and self.peekNext() == '/')

    def isAlpha(self, c: str) -> bool:
        return (('a' <= c <= 'z') or
                ('A' <= c <= 'Z') or
                c == '_')

    def isAlphaNumeric(self, c: str) -> bool:
        return self.isAlpha(c) or self.isDigit(c)

    def isDigit(self, c: str) -> bool:
        return '0' <= c <= '9'

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def advance(self, *, by: int = 1) -> str:
        self.current += by
        return self.source[self.current - by: self.current]

    def addToken(self, type: TT, *, literal: object = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
