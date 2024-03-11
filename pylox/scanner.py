
from loxtoken import Token
from loxtokentype import TokenType as tt

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

        self.tokens.add(Token(tt.EOF, "", None, self.line))
        return self.tokens

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

