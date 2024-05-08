from typing import Protocol
from dataclasses import dataclass
from loxtoken import Token


class Expr(Protocol):
	pass


@dataclass
class Binary(Expr):
	left: Expr
	operator: Token
	right: Expr


@dataclass
class Grouping(Expr):
	expression: Expr


@dataclass
class Literal(Expr):
	value: object


@dataclass
class Unary(Expr):
	operator: Token
	right: Expr


