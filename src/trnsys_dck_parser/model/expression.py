__all__ = [
    "Expression",
    "Variable",
    "FunctionCall",
    "cos",
    "sin"
]

import abc as _abc
import dataclasses as _dc
import typing as _tp

Number = _tp.Union[int, float]

ExpressionOrNumber = _tp.Union["Expression", Number]


class Expression(_abc.ABC):
    def __add__(self, other: ExpressionOrNumber) -> "Addition":
        return _create_binary_expression(Addition, self, other)

    def __radd__(self, other: ExpressionOrNumber) -> "Addition":
        return _create_binary_expression(Addition, other, self)

    def __sub__(self, other: ExpressionOrNumber) -> "Subtraction":
        return _create_binary_expression(Subtraction, self, other)

    def __rsub__(self, other: ExpressionOrNumber) -> "Subtraction":
        return _create_binary_expression(Subtraction, other, self)

    def __mul__(self, other: ExpressionOrNumber) -> "Multiplication":
        return _create_binary_expression(Multiplication, self, other)

    def __rmul__(self, other: ExpressionOrNumber) -> "Multiplication":
        return _create_binary_expression(Multiplication, other, self)

    def __truediv__(self, other: ExpressionOrNumber) -> "Division":
        return _create_binary_expression(Division, self, other)

    def __rtruediv__(self, other: ExpressionOrNumber) -> "Division":
        return _create_binary_expression(Division, other, self)

    def __pow__(self, power: ExpressionOrNumber) -> "Power":
        return _create_binary_expression(Power, self, power)


@_dc.dataclass(frozen=True)
class Literal(Expression):
    value: Number


@_dc.dataclass(frozen=True)
class UnaryExpression(Expression, _abc.ABC):
    x: Expression


@_dc.dataclass(frozen=True)
class BinaryExpression(Expression, _abc.ABC):
    x: Expression
    y: Expression


_T = _tp.TypeVar("_T", bound=BinaryExpression)


def _create_binary_expression(clazz: _tp.Type[_T], x: ExpressionOrNumber, y: ExpressionOrNumber) -> _T:
    xx = _wrap_in_literal_if_number(x)
    yy = _wrap_in_literal_if_number(y)
    return clazz(xx, yy)


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
        return FunctionCall(self.name, *arguments)


class UnaryFunction(FunctionBase, _abc.ABC):
    def __call__(self, x: ExpressionOrNumber):
        return self._call(x)


sin = UnaryFunction("SIN")
cos = UnaryFunction("COS")
