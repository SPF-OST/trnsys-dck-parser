import trnsys_dck_parser.common as _com
import trnsys_dck_parser.parse.common as _pcom


class Regexes:
    POSITIVE_INTEGER = r"[0-9]+"


class Tokens:
    IDENTIFIER = _pcom.TokenDefinition("variable", _com.IDENTIFIER_PATTERN.pattern)
