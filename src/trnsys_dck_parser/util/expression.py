import typing as _tp

import trnsys_dck_parser.model.expression as _model
import trnsys_dck_parser.parse.expression as _parse
import trnsys_dck_parser.parse.common as _pcom


def create_literal(number: _model.Number) -> _model.Literal:
    return _model.Literal(number)


def create_variable(variable: str) -> _model.Variable:
    result = _parse.parse(variable)
    _pcom.raise_if_error(result)

    if not isinstance(result, _model.Variable):
        raise ValueError(f"Invalid variable name.", variable)

    return result


def create_variables(variables: str) -> _tp.Sequence[_model.Variable]:
    return [create_variable(v) for v in variables.split()]
