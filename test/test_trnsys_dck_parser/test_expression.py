import dataclasses as _dc
import typing as _tp

import pytest as _pt

import trnsys_dck_parser as _tdp


@_dc.dataclass
class _ExpressionTestCase:
    string: str
    expected_expression: _tdp.Expression


def _get_expression_test_cases() -> _tp.Iterable[_ExpressionTestCase]:
    string = "0.2"
    expression: _tdp.Expression = _tdp.create_literal(0.2)
    yield _ExpressionTestCase(string, expression)

    string = "7"
    expression = _tdp.create_literal(7)
    yield _ExpressionTestCase(string, expression)

    string = "(1+COS(C_tilt))*0.5*tSky + (1-COS(C_tilt))*0.5*tAmb"
    t_sky, c_tilt, t_amb = _tdp.create_variables("C_tilt tSky tAmb")
    expression = (1 + _tdp.COS(c_tilt)) * 0.5 * t_sky + (1 - _tdp.COS(c_tilt)) * 0.5 * t_amb
    yield _ExpressionTestCase(string, expression)

    string = "((tSky+273.15)**4)*5.67*(10**-8)*3.6"
    t_sky = _tdp.create_variable("tSky")
    expression = (t_sky + 273.15) ** 4 * 5.67 * _tdp.create_literal(10)**-8 * 3.6
    yield _ExpressionTestCase(string, expression)

    string = "numModPv2*PvURefMpp*PvIRefMpp/1000"
    num_mod_pv2, pv_u_ref_mpp, pv_i_ref_mpp = _tdp.create_variables("numModPv2 PvURefMpp PvIRefMpp")
    expression = num_mod_pv2 * pv_u_ref_mpp * pv_i_ref_mpp / 1000
    yield _ExpressionTestCase(string, expression)


def _get_expression_test_params() -> _tp.Sequence[_tp.Any]:
    return [_pt.param(test_case, id=test_case.string) for test_case in _get_expression_test_cases()]


@_pt.mark.parametrize("test_case", _get_expression_test_params())
def test_expression(test_case: _ExpressionTestCase) -> None:
    actual_expression = _tdp.create_expression(test_case.string)

    assert actual_expression == test_case.expected_expression
