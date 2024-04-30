from .. import common as _com
from . import parse as _parse

import trnsys_dck_parser.model.expression as _mexpr

ParserSuccess = _com.ParseSuccess[_mexpr.Expression]
ParserResult = _com.ParseResult[_mexpr.Expression]


def parse_expression(expression: str) -> ParserResult:
    parser = _parse.Parser(expression)
    return parser.parse()
