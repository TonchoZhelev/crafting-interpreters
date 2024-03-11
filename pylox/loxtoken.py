from dataclasses import dataclass

from loxtokentype import TokenType

@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int
