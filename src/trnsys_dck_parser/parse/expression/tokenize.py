import trnsys_dck_parser.parse.tokens as _ptok

from .. import common as _com


class Tokens:
    POSITIVE_INTEGER = _com.TokenDefinition("positive integer", _ptok.Regexes.POSITIVE_INTEGER, priority=1)
    NEGATIVE_INTEGER = _com.TokenDefinition("integer", r"-[0-9]+", priority=2)
    FLOAT = _com.TokenDefinition("floating point number", r"-?[0-9]*\.[0-9]+([eE]-?[0-9]+)?", priority=3)
    LEFT_SQUARE_BRACKET = _com.TokenDefinition('opening square bracket ("[")', r"\[")
    RIGHT_SQUARE_BRACKET = _com.TokenDefinition('closing square bracket ("]")', r"\]")
    COMMA = _com.TokenDefinition('comma (",")', r",")
    PLUS = _com.TokenDefinition('plus ("+")', r"\+")
    MINUS = _com.TokenDefinition('minus ("-")', r"-")
    TIMES = _com.TokenDefinition('times ("*")', r"\*", priority=1)
    DIVIDE = _com.TokenDefinition('division by ("/")', r"/")
    POWER = _com.TokenDefinition('raise by ("**")', r"\*\*", priority=2)
    LEFT_PAREN = _com.TokenDefinition('opening parenthesis ("(")', r"\(")
    RIGHT_PAREN = _com.TokenDefinition('closing parenthesis (")")', r"\)")


def create_lexer(input_string: str) -> _com.Lexer:
    token_definitions = [
        Tokens.POSITIVE_INTEGER,
        Tokens.NEGATIVE_INTEGER,
        Tokens.FLOAT,
        Tokens.LEFT_SQUARE_BRACKET,
        Tokens.RIGHT_SQUARE_BRACKET,
        Tokens.COMMA,
        _ptok.Tokens.IDENTIFIER,
        Tokens.PLUS,
        Tokens.MINUS,
        Tokens.TIMES,
        Tokens.DIVIDE,
        Tokens.POWER,
        Tokens.LEFT_PAREN,
        Tokens.RIGHT_PAREN,
    ]

    return _com.Lexer(input_string, token_definitions)
