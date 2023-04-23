__all__ = [
    "ExpressionOrNumber",
    "Variable",
    "FunctionCall",
    "cos",
    "create_variable",
    "create_variables",
]

import abc as _abc
import dataclasses as _dc
import typing as _tp

import trnsys_dck_parser.common as _pcom


Number = int | float

ExpressionOrNumber = _tp.Union["Expression", Number]


class Expression(_abc.ABC):
    def __add__(self, other: ExpressionOrNumber) -> "Addition":
        return Addition(self, other)

    def __radd__(self, other: ExpressionOrNumber) -> "Addition":
        return Addition(other, self)

    def __sub__(self, other: ExpressionOrNumber) -> "Subtraction":
        return Subtraction(self, other)

    def __rsub__(self, other: ExpressionOrNumber) -> "Subtraction":
        return Subtraction(other, self)

    def __mul__(self, other: ExpressionOrNumber) -> "Multiplication":
        return Multiplication(self, other)

    def __rmul__(self, other: ExpressionOrNumber) -> "Multiplication":
        return Multiplication(other, self)

    def __truediv__(self, other: ExpressionOrNumber) -> "Division":
        return Division(self, other)

    def __rtruediv__(self, other: ExpressionOrNumber) -> "Division":
        return Division(self, other)

    def __pow__(self, power: ExpressionOrNumber) -> "Power":
        return Power(self, power)


@_dc.dataclass(frozen=True)
class Literal(Expression):
    value: Number


@_dc.dataclass(frozen=True)
class UnaryExpression(Expression, _abc.ABC):
    x: Expression

    @staticmethod
    def create(x: ExpressionOrNumber) -> "UnaryExpression":
        return UnaryExpression(_wrap_in_literal_if_number(x))


@_dc.dataclass(frozen=True)
class BinaryExpression(Expression, _abc.ABC):
    x: Expression
    y: Expression

    @staticmethod
    def create(x: ExpressionOrNumber, y: ExpressionOrNumber) -> "BinaryExpression":
        return BinaryExpression(
            _wrap_in_literal_if_number(x),
            _wrap_in_literal_if_number(y)
        )


def _wrap_in_literal_if_number(x: ExpressionOrNumber) -> Expression:
    if isinstance(x, Expression):
        return x

    return Literal(x)


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


@_dc.dataclass(frozen=True)
class Variable(Expression):
    name: str

    def __post_init__(self):
        pattern = _pcom.IDENTIFIER_PATTERN
        if not pattern.fullmatch(self.name):
            raise ValueError(f"Variable names must match the following regex pattern: {pattern.pattern}")


@_dc.dataclass(frozen=True)
class UnitOutput(Expression):
    unit_number: int
    output_number: int


@_dc.dataclass(frozen=True)
class FunctionCall(Expression):
    function: str
    arguments: _tp.Sequence[ExpressionOrNumber]


@_dc.dataclass(frozen=True)
class FunctionBase(_abc.ABC):
    name: str

    def _call(self, *arguments: ExpressionOrNumber) -> Expression:
        return FunctionCall(self.__class__.__name__, *arguments)


class UnaryFunction(FunctionBase, _abc.ABC):
    def __call__(self, x: ExpressionOrNumber):
        return self._call(x)


sin = UnaryFunction("sin")
cos = UnaryFunction("cos")


def create_literal(literal: Number) -> Number:
    return literal


def create_variable(variable: str) -> Variable:
    return Variable(variable)


def create_variables(variables: str) -> _tp.Sequence[Variable]:
    return [Variable(v) for v in variables.split()]
