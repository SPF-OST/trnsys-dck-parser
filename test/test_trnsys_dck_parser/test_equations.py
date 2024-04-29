import trnsys_dck_parser as _parser
import trnsys_dck_parser.build as _build
import trnsys_dck_parser.model.equations as _meqs


def test_equations_without_placeholders() -> None:
    equations_string = r"""\
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
    actual_equations = _parser.parse_equations(equations_string)

    expected_n_equations = 9

    all_expected_equations = [
        _build.create_equation("dpAuxSH_bar", "0.2"),
        _build.create_equation("PflowAuxSH_W", "((MfrAuxOut/3600)/RhoWat)*dpAuxSH_bar*100000"),
        _build.create_equation("etaPuAuxSh", "0.35"),
        _build.create_equation("PelPuAuxSH_kW", "(PflowAuxSH_W/1000)/etaPuAuxSH"),
        _build.create_equation("dpAuxBrine_bar", "0.3"),
        _build.create_equation("PflowAuxBrine_W", "((MfrAuxEvapOut/3600)/RhoBri)*dpAuxBrine_bar*100000"),
        _build.create_equation("etaPuAuxBrine", "0.35"),
        _build.create_equation("PelPuAuxBrine_kW", "(PflowAuxBrine_W/1000)/etaPuAuxBrine"),
        _build.create_equation("PelPuAuxBri_kW", "GT(MfrEvapIn,0.1)*PelPuAuxBrine_kW"),
    ]

    expected_equations = _meqs.Equations(expected_n_equations, all_expected_equations)

    assert actual_equations == expected_equations

    # TODO: check whether comments were parsed correctly
    assert actual_equations.comments == [_deck.InlineComment("foo", line=5, column=0)]
