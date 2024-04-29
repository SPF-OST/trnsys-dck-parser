import trnsys_dck_parser.model.equations as _meqs
import trnsys_dck_parser.model.expression as _mexpr
import trnsys_dck_parser.parse.expression as _pexpr

import typing as _tp


def create_equation(variable_name: str, rhs: str) -> _meqs.Equation:
    rhs = _pexpr.parse(rhs)
    return _meqs.Equation(variable_name, rhs)


def create_literal(number: _mexpr.Number) -> _mexpr.Literal:
    return _mexpr.Literal(number)


def create_variable(variable: str) -> _mexpr.Variable:
    return _mexpr.Variable(variable)


def create_variables(variables: str) -> _tp.Sequence[_mexpr.Variable]:
    return [_mexpr.Variable(v) for v in variables.split()]
