import abc as _abc
import dataclasses as _dc
import typing as _tp

import trnsys_dck_parser.model.equations as _meqs
import trnsys_dck_parser.model.expression as _mexpr
import trnsys_dck_parser.parse.common as _pcom
import trnsys_dck_parser.parse.expression.parse as _pexpp


def create_equation(variable_name: str, rhs: str) -> _meqs.Equation:
    parse_result = parse_expression(rhs)
    equation = _pcom.success(parse_result).value
    return _meqs.Equation(variable_name, equation)


def create_literal(number: _mexpr.Number) -> _mexpr.Literal:
    return _mexpr.Literal(number)


def create_variable(variable: str) -> _mexpr.Variable:
    return _mexpr.Variable(variable)


def create_variables(variables: str) -> _tp.Sequence[_mexpr.Variable]:
    return [_mexpr.Variable(v) for v in variables.split()]


@_dc.dataclass(eq=True)
class FunctionBase(_abc.ABC):
    name: str

    def _call(self, *arguments: _mexpr.Expression) -> _mexpr.Expression:
        return _mexpr.FunctionCall(self.name, list(arguments))


class UnaryFunction(FunctionBase, _abc.ABC):
    def __call__(self, x: _mexpr.Expression):
        return self._call(x)


sin = UnaryFunction("SIN")
cos = UnaryFunction("COS")


def parse_expression(expression: str) -> _pexpp.ParseResult:
    parser = _pexpp.Parser(expression)
    return parser.parse()
