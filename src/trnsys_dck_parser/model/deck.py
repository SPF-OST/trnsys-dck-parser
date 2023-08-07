__all__ = ["Deck", "Equations", "InlineComment"]

import dataclasses as _dc
import typing as _tp


class Deck:
    def add_equations(self) -> "Equations":
        return Equations()


class Equations:
    def add_equation(self, variable: str, expression: str) -> None:
        pass

    @property
    def comments(self) -> _tp.Sequence["Comment"]:
        return []


@_dc.dataclass
class Comment:
    comment: str
    line: int
    column: int


class InlineComment(Comment):
    pass


