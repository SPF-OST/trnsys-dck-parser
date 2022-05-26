__all__ = [
    "Expression",
    "Literal",
    "Variable",
    "Function",
    "COS",
    "create_literal",
    "create_variable",
    "create_variables",
]

import typing as _tp


Number = _tp.Union[int, float]

ExpressionOrNumber = _tp.Union["Expression", Number]


class Expression:
    def __add__(self, other: ExpressionOrNumber) -> "Addition":
        return Addition()

    def __radd__(self, other: ExpressionOrNumber) -> "Addition":
        return Addition()

    def __sub__(self, other: ExpressionOrNumber) -> "Subtraction":
        return Subtraction()

    def __rsub__(self, other: ExpressionOrNumber) -> "Subtraction":
        return Subtraction()

    def __mul__(self, other: ExpressionOrNumber) -> "Multiplication":
        return Multiplication()

    def __rmul__(self, other: ExpressionOrNumber) -> "Multiplication":
        return Multiplication()

    def __truediv__(self, other: ExpressionOrNumber) -> "Division":
        return Division()

    def __rtruediv__(self, other: ExpressionOrNumber) -> "Division":
        return Division()

    def __pow__(self, power: ExpressionOrNumber, modulo=None) -> "Power":
        return Power()


class Addition(Expression):
    pass


class Subtraction(Expression):
    pass


class Multiplication(Expression):
    pass


class Division(Expression):
    pass


class Power(Expression):
    pass


class Literal(Expression):
    pass


class Variable(Expression):
    pass


class Function(Expression):
    def __call__(self, *args: ExpressionOrNumber) -> Expression:
        return Expression()


COS = Function()


def create_literal(literal: _tp.Union[int, float]) -> Literal:
    return Literal()


def create_variable(variable: str) -> Variable:
    return Variable()


def create_variables(variables: str) -> _tp.Sequence[Variable]:
    return []


