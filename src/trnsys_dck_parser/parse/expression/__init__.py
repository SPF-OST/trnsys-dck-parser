import trnsys_dck_parser.model.expression as _exp
import trnsys_dck_parser.parse.common as _com

from . import parse as _parse


def parse(expression: str) -> _com.ParserResult[_exp.Expression]:
    parser = _parse.Parser(expression)
    return parser.parse()
