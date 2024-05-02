import abc as _abc
import dataclasses as _dc
import typing as _tp

import trnsys_dck_parser.common as _pcom


class Expression(_abc.ABC):
    def __neg__(self) -> "Negation":
        return Negation(self)

    def __add__(self, other: "Expression") -> "Addition":
        return Addition(self, other)

    def __radd__(self, other: "Expression") -> "Addition":
        return Addition(other, self)

    def __sub__(self, other: "Expression") -> "Subtraction":
        return Subtraction(self, other)

    def __rsub__(self, other: "Expression") -> "Subtraction":
        return Subtraction(other, self)

    def __mul__(self, other: "Expression") -> "Multiplication":
        return Multiplication(self, other)

    def __rmul__(self, other: "Expression") -> "Multiplication":
        return Multiplication(other, self)

    def __truediv__(self, other: "Expression") -> "Division":
        return Division(self, other)

    def __rtruediv__(self, other: "Expression") -> "Division":
        return Division(self, other)

    def __pow__(self, power: "Expression") -> "Power":
        return Power(self, power)


Number = int | float


@_dc.dataclass(eq=True)
class Literal(Expression):
    value: Number


@_dc.dataclass(eq=True)
class UnaryExpression(Expression, _abc.ABC):
    x: Expression


@_dc.dataclass(eq=True)
class Negation(UnaryExpression):
    pass


@_dc.dataclass(eq=True)
class BinaryExpression(Expression, _abc.ABC):
    x: Expression
    y: Expression


class Addition(BinaryExpression):
    pass


class Subtraction(BinaryExpression):
    pass


class Multiplication(BinaryExpression):
    pass


class Division(BinaryExpression):
    pass


class Power(BinaryExpression):
    pass


@_dc.dataclass(eq=True)
class Variable(Expression):
    name: str

    def __post_init__(self):
        pattern = _pcom.IDENTIFIER_PATTERN
        if not pattern.fullmatch(self.name):
            raise ValueError(f"Variable names must match the following regex pattern: {pattern.pattern}")


@_dc.dataclass(eq=True)
class UnitOutput(Expression):
    unit_number: int
    output_number: int


@_dc.dataclass(eq=True)
class FunctionCall(Expression):
    function: str
    arguments: _tp.Sequence[Expression]
