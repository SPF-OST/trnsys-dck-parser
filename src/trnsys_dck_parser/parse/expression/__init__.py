from trnsys_dck_parser import deck as _dck

from .. import common as _com
from . import parse as _parse


def parse(expression: str) -> _com.ParserResult[_dck.ExpressionOrNumber]:
    parser = _parse.Parser(expression)
    return parser.parse()
