__all__ = ["parse_expression", "parse_equations"]

from .parse.deck import parse_equations

from .parse.expression import parse as parse_expression
