import abc as _abc
import dataclasses as _dc
import re as _re
import typing as _tp


@_dc.dataclass
class ParseError:
    error_message: str
    input_string: str
    error_start: int

    @property
    def error_string(self) -> str:
        return self.input_string[self.error_start :]

    def __repr__(self) -> str:
        return f"Parse error: {self.error_message}: {self.error_string[:10]}"


_TCo = _tp.TypeVar("_TCo", covariant=True)
_SCo = _tp.TypeVar("_SCo", covariant=True)


@_dc.dataclass
class ParseSuccess(_tp.Generic[_TCo]):
    value: _TCo
    remaining_string_input_start_index: int


ParseResult = ParseSuccess[_TCo] | ParseError


def is_success(result: ParseResult) -> bool:
    return isinstance(result, ParseSuccess)


def success(result: ParseResult[_TCo]) -> ParseSuccess[_TCo]:
    if not is_success(result):
        raise ValueError(f"Not a success: {result.error_message}.")

    return _tp.cast(ParseSuccess[_TCo], result)


def error(result: ParseResult[_TCo]) -> ParseError:
    if is_success(result):
        raise ValueError(f"Not a failure: {result.error_message}.")

    return _tp.cast(ParseError, result)


@_dc.dataclass
class TokenDefinition:
    description: str
    pattern: _re.Pattern = _dc.field(init=False)
    regex: _dc.InitVar[str]
    flags: _re.RegexFlag = _re.RegexFlag.NOFLAG

    # For tokens with "overlapping" patterns, the one with the higher priority
    # will be tried to match first
    priority: int = -1

    def __post_init__(self, regex: str) -> None:
        self.pattern = _re.compile(regex, self.flags)


class Tokens:
    END = TokenDefinition("end of input", r"$")


@_dc.dataclass
class Token:
    definition: TokenDefinition
    value: str
    input_string: str
    start_index_inclusive: int
    end_index_exclusive: int


LexerResult = Token | ParseError


@_dc.dataclass
class ParseErrorException(Exception):
    parse_error: ParseError


class _Ignore:
    _IGNORE_REGEXES = "|".join(
        [
            r"[ \t\n]+",  # Whitespace
            r"(?m:!.*$)",  # Comment
        ]
    )

    Pattern = _re.compile(_IGNORE_REGEXES, _re.RegexFlag.MULTILINE)


class Lexer:
    def __init__(self, input_string: str, token_definitions: _tp.Sequence[TokenDefinition]) -> None:
        self.input_string = input_string

        def get_priority(token_definition: TokenDefinition) -> int:
            return token_definition.priority

        self._token_definitions = [
            *sorted(token_definitions, key=get_priority, reverse=True),
            Tokens.END,
        ]
        self.current_pos = 0

    @property
    def remaining_input(self) -> str:
        return self.input_string[self.current_pos :]

    def get_next_token(self) -> LexerResult:
        while match := self._match(_Ignore.Pattern):
            self.advance_input(match.end())

        for token_definition in self._token_definitions:
            match = self._match(token_definition.pattern)
            if match:
                self.advance_input(match.end())
                token = Token(token_definition, match.group(), self.input_string, match.start(), match.end())
                return token

        parsing_error = ParseError(
            "Not a recognized token.",
            self.input_string,
            self.current_pos,
        )

        return parsing_error

    def _match(self, pattern: _re.Pattern) -> _re.Match:
        match = pattern.match(self.input_string, pos=self.current_pos)
        return match

    def advance_input(self, to: int) -> None:
        if to < self.current_pos:
            return

        self.current_pos = to


class ParserBase(_tp.Generic[_TCo], _abc.ABC):
    def __int__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: _tp.Optional[Token] = None
        self._remaining_input_string_start_index = 0

    @property
    def _remaining_input_string(self) -> str:
        return self._lexer.input_string[self._remaining_input_string_start_index :]

    def _accept(self, token_definition: TokenDefinition) -> str | None:
        if not self._current_token:
            self._set_next_token()

        if self._current_token.definition != token_definition:
            return None

        self._remaining_input_string_start_index = self._current_token.end_index_exclusive
        value = self._current_token.value

        self._current_token = None

        return value

    def _expect(self, token_definition: TokenDefinition) -> str:
        value = self._accept(token_definition)
        if value is not None:
            return value

        expected_token = token_definition.description

        self._raise_parsing_error(f"Expected {expected_token} but found {{actual_token}}.")

    def _expect_sub_parser(self, parser: "ParserBase[_SCo]") -> _SCo:
        result = parser.parse()
        if not is_success(result):
            raise ParseErrorException(result)

        remaining_string_input_start_index = (
            self._remaining_input_string_start_index + result.remaining_string_input_start_index
        )
        self._advance_input(remaining_string_input_start_index)

        return result.value

    def _set_next_token(self) -> None:
        next_token = self._lexer.get_next_token()
        if isinstance(next_token, ParseError):
            raise ParseErrorException(next_token)
        self._current_token = next_token

    def _advance_input(self, to: int) -> None:
        self._remaining_input_string_start_index = to
        self._lexer.advance_input(to)

    def _raise_parsing_error(self, error_message: str, actual_token_key: str = "actual_token") -> _tp.NoReturn:
        assert self._current_token

        actual_token_description = self._current_token.definition.description

        formatted_error_message = error_message.format(**{actual_token_key: actual_token_description})

        parsing_error = ParseError(
            formatted_error_message, self._lexer.input_string, self._current_token.start_index_inclusive
        )

        raise ParseErrorException(parsing_error)

    @_abc.abstractmethod
    def parse(self) -> ParseResult:
        raise NotImplementedError()
