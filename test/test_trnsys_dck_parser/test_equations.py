import trnsys_dck_parser as _tdp


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
    actual_equations = _tdp.create_equations(equations_string)

    expected_equations = _tdp.Equations()

    expected_equations.add_equation("dpAuxSH_bar", "0.2")
    expected_equations.add_equation("PflowAuxSH_W", "((MfrAuxOut/3600)/RhoWat)*dpAuxSH_bar*100000")
    expected_equations.add_equation("etaPuAuxSh", "0.35")
    expected_equations.add_equation("PelPuAuxSH_kW", "(PflowAuxSH_W/1000)/etaPuAuxSH")
    expected_equations.add_equation("dpAuxBrine_bar", "0.3")
    expected_equations.add_equation("PflowAuxBrine_W", "((MfrAuxEvapOut/3600)/RhoBri)*dpAuxBrine_bar*100000")
    expected_equations.add_equation("etaPuAuxBrine", "0.35")
    expected_equations.add_equation("PelPuAuxBrine_kW", "(PflowAuxBrine_W/1000)/etaPuAuxBrine")
    expected_equations.add_equation("PelPuAuxBri_kW", "GT(MfrEvapIn,0.1)*PelPuAuxBrine_kW")

    assert actual_equations == expected_equations

    # TODO: check whether comments were parsed correctly
    assert actual_equations.comments == [_tdp.InlineComment("foo", line=5, column=0)]
