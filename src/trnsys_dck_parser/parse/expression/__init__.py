from .. import common as _com
from . import parse as _parse

import trnsys_dck_parser.model.expression as _mexpr

ParserResult = _com.ParserResult[_mexpr.Expression]


def parse(expression: str) -> ParserResult:
    parser = _parse.Parser(expression)
    return parser.parse()
