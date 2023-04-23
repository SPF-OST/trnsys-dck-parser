import trnsys_dck_parser.common as _pcom

from .. import common as _com


class Tokens:
    INTEGER = _com.TokenDefinition("INTEGER", r"-?[0-9]+", priority=2)
    FLOAT = _com.TokenDefinition("FLOAT", r"-?[0-9]*\.[0-9]+([eE]-?[0-9]+)?", priority=1)
    LEFT_SQUARE_BRACKET = _com.TokenDefinition("LEFT_SQUARE_BRACKET", r"\[")
    RIGHT_SQUARE_BRACKET = _com.TokenDefinition("RIGHT_SQUARE_BRACKET", r"\]")
    COMMA = _com.TokenDefinition("COMMA", r",")
    IDENTIFIER = _com.TokenDefinition("IDENTIFIER", _pcom.IDENTIFIER_PATTERN.pattern)
    PLUS = _com.TokenDefinition("PLUS", r"\+")
    MINUS = _com.TokenDefinition("MINUS", r"-")
    TIMES = _com.TokenDefinition("TIMES", r"\*")
    DIVIDE = _com.TokenDefinition("DIVIDE", r"/")
    LEFT_PAREN = _com.TokenDefinition("LEFT_PAREN", r"\(")
    RIGHT_PAREN = _com.TokenDefinition("RIGHT_PAREN", r"\)")


def create_lexer(input_string: str) -> _com.Lexer:
    token_definitions = [
        Tokens.INTEGER,
        Tokens.FLOAT,
        Tokens.LEFT_SQUARE_BRACKET,
        Tokens.RIGHT_SQUARE_BRACKET,
        Tokens.COMMA,
        Tokens.IDENTIFIER,
        Tokens.PLUS,
        Tokens.MINUS,
        Tokens.TIMES,
        Tokens.DIVIDE,
        Tokens.LEFT_PAREN,
        Tokens.RIGHT_PAREN,
    ]

    return _com.Lexer(input_string, token_definitions)
