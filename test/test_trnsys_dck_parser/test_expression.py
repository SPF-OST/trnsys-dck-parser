import dataclasses as _dc
import typing as _tp

import pytest as _pt

import trnsys_dck_parser as _parser
import trnsys_dck_parser.deck as _deck


@_dc.dataclass
class _ExpressionTestCase:
    string: str
    expected_expression: _deck.ExpressionOrNumber


def _get_expression_test_cases() -> _tp.Iterable[_ExpressionTestCase]:
    string = "0.2"
    expression = 0.2
    yield _ExpressionTestCase(string, expression)

    string = "7"
    expression = 7
    yield _ExpressionTestCase(string, expression)

    string = "(1+COS(C_tilt))*0.5*tSky + (1-COS(C_tilt))*0.5*tAmb"
    t_sky, c_tilt, t_amb = _deck.create_variables("tSky C_tilt tAmb")
    expression = (1 + _deck.cos(c_tilt)) * 0.5 * t_sky + (1 - _deck.cos(c_tilt)) * 0.5 * t_amb
    yield _ExpressionTestCase(string, expression)

    string = "((tSky+273.15)**4)*5.67*(10**-8)*3.6"
    t_sky = _deck.create_variable("tSky")
    expression = (t_sky + 273.15) ** 4 * 5.67 * _deck.create_literal(10) ** -8 * 3.6
    yield _ExpressionTestCase(string, expression)

    string = "numModPv2*PvURefMpp*PvIRefMpp/1000"
    num_mod_pv2, pv_u_ref_mpp, pv_i_ref_mpp = _deck.create_variables("numModPv2 PvURefMpp PvIRefMpp")
    expression = num_mod_pv2 * pv_u_ref_mpp * pv_i_ref_mpp / 1000
    yield _ExpressionTestCase(string, expression)

    string = "numModPv2"
    expression = _deck.create_variable("numModPv2")
    yield _ExpressionTestCase(string, expression)

    string = "numModPv2/-uvw"
    num_mod_pv2, uvw = _deck.create_variables("numModPv2 uvw")
    expression = num_mod_pv2 / -uvw
    yield _ExpressionTestCase(string, expression)

    string = "x*y**z"
    x, y, z = _deck.create_variables("x y z")
    expression = x * (y**z)
    yield _ExpressionTestCase(string, expression)

    string = ""
    expression = _parser.ParsingError(
        error_message="Expected number, variable, function call, opening "
        "square bracket or opening parenthesis but found "
        "end of input",
        input_string=string,
        error_start=len(string) - 1,
    )
    yield _ExpressionTestCase(string, expression)

    string = "((tSky+)"
    expression = _parser.ParsingError(
        error_message="Expected number, variable, function call, opening "
        "square bracket or opening parenthesis but found "
        'closing parenthesis (")")',
        input_string=string,
        error_start=len(string) - 1,
    )
    yield _ExpressionTestCase(string, expression)

    string = "(10**-8"
    expression = _parser.ParsingError(
        error_message='Expected closing parenthesis (")") but found end of input.',
        input_string=string,
        error_start=len(string),
    )
    yield _ExpressionTestCase(string, expression)

    string = "(10**-)"
    expression = _parser.ParsingError(
        error_message="Expected number, variable, function call, opening "
        "square bracket or opening parenthesis but found "
        'closing parenthesis (")")',
        input_string=string,
        error_start=len(string) - 2,
    )
    yield _ExpressionTestCase(string, expression)

    string = "foobar 10"
    expression = _deck.create_variable("foobar")
    yield _ExpressionTestCase(string, expression)


@_pt.mark.parametrize("test_case", _get_expression_test_cases(), ids=lambda etc: etc.string)
def test_expression(test_case: _ExpressionTestCase) -> None:
    actual_expression = _parser.parse_expression(test_case.string)

    assert actual_expression == test_case.expected_expression
