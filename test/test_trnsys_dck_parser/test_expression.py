import dataclasses as _dc
import typing as _tp

import pytest as _pt

import trnsys_dck_parser.build as _build
import trnsys_dck_parser.model.expression as _mexpr
import trnsys_dck_parser.parse.common as _pcom
import trnsys_dck_parser.parse.expression.parse as _pexpr

_l = _build.create_literal


@_dc.dataclass
class _ExpressionTestCase:
    string: str
    parser_result: _pexpr.ParseResult
    benchmark: bool = True


def _get_expression_test_cases() -> _tp.Iterable[_ExpressionTestCase]:
    result: _pcom.ParseResult[_mexpr.Expression]

    string = "0.2"
    result = _pcom.ParseSuccess(_mexpr.Literal(0.2), 3)
    yield _ExpressionTestCase(string, result, benchmark=False)

    string = "7"
    result = _pcom.ParseSuccess(_mexpr.Literal(7), 1)
    yield _ExpressionTestCase(string, result, benchmark=False)

    string = "(1+COS(C_tilt))*0.5*tSky + (1-COS(C_tilt))*0.5*tAmb"
    t_sky, c_tilt, t_amb = _build.create_variables("tSky C_tilt tAmb")
    result = _pcom.ParseSuccess(
        (_l(1) + _build.cos(c_tilt)) * _l(0.5) * t_sky + (_l(1) - _build.cos(c_tilt)) * _l(0.5) * t_amb,
        51,
    )
    yield _ExpressionTestCase(string, result)

    string = "((tSky+273.15)**4)*5.67*(10**-8)*3.6"
    t_sky = _build.create_variable("tSky")
    result = _pcom.ParseSuccess(
        (t_sky + _l(273.15)) ** _l(4) * _l(5.67) * _l(10) ** _l(-8) * _l(3.6),
        36,
    )
    yield _ExpressionTestCase(string, result)

    string = "numModPv2*PvURefMpp*PvIRefMpp/1000"
    num_mod_pv2, pv_u_ref_mpp, pv_i_ref_mpp = _build.create_variables("numModPv2 PvURefMpp PvIRefMpp")
    result = _pcom.ParseSuccess(num_mod_pv2 * pv_u_ref_mpp * pv_i_ref_mpp / _l(1000), 34)
    yield _ExpressionTestCase(string, result)

    string = "numModPv2"
    result = _pcom.ParseSuccess(
        _build.create_variable("numModPv2"),
        9,
    )
    yield _ExpressionTestCase(string, result, benchmark=False)

    string = "numModPv2/-uvw"
    num_mod_pv2, uvw = _build.create_variables("numModPv2 uvw")
    result = _pcom.ParseSuccess(num_mod_pv2 / -uvw, 14)
    yield _ExpressionTestCase(string, result, benchmark=False)

    string = "x*y**z"
    x, y, z = _build.create_variables("x y z")
    result = _pcom.ParseSuccess(x * (y ** z), 6)
    yield _ExpressionTestCase(string, result, benchmark=False)

    string = ""
    result = _pcom.ParseError(
        error_message="Expected number, variable, function call, opening "
                      "square bracket or opening parenthesis but found "
                      "end of input",
        input_string=string,
        error_start=0,
    )
    yield _ExpressionTestCase(string, result, benchmark=False)

    string = "((tSky+)"
    result = _pcom.ParseError(
        error_message="Expected number, variable, function call, opening "
                      "square bracket or opening parenthesis but found "
                      'closing parenthesis (")")',
        input_string=string,
        error_start=7,
    )
    yield _ExpressionTestCase(string, result, benchmark=False)

    string = "(10**-8"
    result = _pcom.ParseError(
        error_message='Expected closing parenthesis (")") but found end of input.',
        input_string=string,
        error_start=7,
    )
    yield _ExpressionTestCase(string, result, benchmark=False)

    string = "(10**-)"
    result = _pcom.ParseError(
        error_message="Expected number, variable, function call, opening "
                      "square bracket or opening parenthesis but found "
                      'closing parenthesis (")")',
        input_string=string,
        error_start=6,
    )
    yield _ExpressionTestCase(string, result, benchmark=False)

    string = "foobar 10"
    result = _pcom.ParseSuccess(_build.create_variable("foobar"), 6)
    yield _ExpressionTestCase(string, result, benchmark=False)


@_pt.mark.parametrize("test_case", _get_expression_test_cases(), ids=lambda etc: etc.string)
def test_expression(test_case: _ExpressionTestCase, benchmark) -> None:
    if test_case.benchmark:
        actual_expression = benchmark(_build.parse_expression, test_case.string)
    else:
        actual_expression = _build.parse_expression(test_case.string)

    assert actual_expression == test_case.parser_result
