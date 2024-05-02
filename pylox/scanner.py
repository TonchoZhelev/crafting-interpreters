from loxtoken import Token
from loxtokentype import TokenType as TT
import lox as Lox


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
                else:
                    self.addToken(TT.SLASH)
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self.line = self.line + 1
            case _:
                Lox.error(self.line, "Unexpected character.")

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


    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)


    def advance(self) -> str:
        self.current += 1
        return self.source[self.current]


    def addToken(self, type: TT) -> None:
        self.addTokenWithLiteral(type, None)


    def addTokenWithLiteral(self, type: TT, literal: object) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    
