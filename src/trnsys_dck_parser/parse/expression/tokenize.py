import trnsys_dck_parser.parse.common as _pcom
import trnsys_dck_parser.parse.tokens as _ptok


class Tokens:
    POSITIVE_INTEGER = _pcom.TokenDefinition("positive integer", _ptok.Regexes.POSITIVE_INTEGER, priority=1)
    NEGATIVE_INTEGER = _pcom.TokenDefinition("integer", r"-[0-9]+", priority=2)
    FLOAT = _pcom.TokenDefinition("floating point number", r"-?[0-9]*\.[0-9]+([eE]-?[0-9]+)?", priority=3)
    LEFT_SQUARE_BRACKET = _pcom.TokenDefinition('opening square bracket ("[")', r"\[")
    RIGHT_SQUARE_BRACKET = _pcom.TokenDefinition('closing square bracket ("]")', r"\]")
    COMMA = _pcom.TokenDefinition('comma (",")', r",")
    PLUS = _pcom.TokenDefinition('plus ("+")', r"\+")
    MINUS = _pcom.TokenDefinition('minus ("-")', r"-")
    TIMES = _pcom.TokenDefinition('times ("*")', r"\*", priority=1)
    DIVIDE = _pcom.TokenDefinition('division by ("/")', r"/")
    POWER = _pcom.TokenDefinition('raise by ("**")', r"\*\*", priority=2)
    LEFT_PAREN = _pcom.TokenDefinition('opening parenthesis ("(")', r"\(")
    RIGHT_PAREN = _pcom.TokenDefinition('closing parenthesis (")")', r"\)")


def create_lexer(input_string: str, start_pos: int) -> _pcom.Lexer:
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

    return _pcom.Lexer(input_string, token_definitions, start_pos)
