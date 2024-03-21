from loxtoken import Token
from loxtokentype import TokenType as TT


class Scanner:

    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []

        self.start: int = 0
        self.current: int = 0
        self.line: int = 1


    def scanTokens(self) -> list[Token]:
        while not isAtEnd():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            scanToken()

        self.tokens.add(Token(TT.EOF, "", None, self.line))
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


    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)


    def advance(self) -> str:
        self.current += 1
        return self.source[self.current]


    def addToken(self, type: TT) -> None:
        addToken(type, null)


    def addTokenWithLiteral(self, type: TT, literal: object) -> None:
        text = self.source[self.start, self.current]
        self.tokens.push(Token(type, text, literal, self.line))

    
