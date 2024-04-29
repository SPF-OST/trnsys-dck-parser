import dataclasses as _dc

import trnsys_dck_parser.model.expression as _expr


@_dc.dataclass
class Equations:
    n_equations: int | None
    equations: list["Equation"]


@_dc.dataclass
class Equation:
    variable_name: str
    rhs: _expr.Expression
