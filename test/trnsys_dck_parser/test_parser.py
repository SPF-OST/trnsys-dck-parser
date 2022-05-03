import pytest as _pt

import trnsys_dck_parser as _tdp


@_pt.fixture(name="parser")
def fixture_parser() -> _tdp.Parser:
    return _tdp.Parser()


def test_equations_without_placeholders(parser: _tdp.Parser) -> None:
    dck_snippet = r"""\
EQUATIONS 9		! 16     
dpAuxSH_bar = 0.2															! according to MacSheep report 7.2 
PflowAuxSH_W = ((MfrAuxOut/3600)/RhoWat)*dpAuxSH_bar*100000					! required power to drive the flow, W
etaPuAuxSh = 0.35															! Assumption
PelPuAuxSH_kW = (PflowAuxSH_W/1000)/etaPuAuxSH								! required pump electric power, kW
dpAuxBrine_bar = 0.3														! assumption (pressure drop is a mix between SH- and Borehole-Loop according to MacSheep report 7.2)
PflowAuxBrine_W = ((MfrAuxEvapOut/3600)/RhoBri)*dpAuxBrine_bar*100000		! required power to drive the flow, W
etaPuAuxBrine = 0.35														! Assumption
PelPuAuxBrine_kW = (PflowAuxBrine_W/1000)/etaPuAuxBrine						! required pump electric power, kW
PelPuAuxBri_kW = GT(MfrEvapIn,0.1)*PelPuAuxBrine_kW							! GT(MfrcondIn,0.1)*PelPuAuxBrine_kW		! naming could be better
"""
    actual_deck = parser.loads(dck_snippet)

    expected_deck = _tdp.Deck()

    equations = expected_deck.add_equations()

    equations.add_equation("etaPuAuxSh", 0.35)

    mfr_aux_out, rho_wat, dp_aux_sh_bar = _tdp.make_vars("mfrAuxOut RhoWat dpAuxSH_bar")
    rhs2 = ((mfr_aux_out / 3600) / rho_wat) * dp_aux_sh_bar * 100_000
    lhs2 = _tdp.make_vars("PflowAuxSH_W")
    equations.add_equation(lhs2, rhs2)

    # ...

    assert actual_deck == expected_deck

    # TODO: check whether comments were parsed correctly
