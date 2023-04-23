import abc as _abc
import dataclasses as _dc
import re as _re
import typing as _tp


@_dc.dataclass
class ParsingError:
    error_message: str
    input_string: str
    error_start: int
    error_end: _tp.Optional[int] = None


_TCo = _tp.TypeVar("_TCo", covariant=True)

ParserResult = _TCo | ParsingError


@_dc.dataclass
class TokenDefinition:
    name: str
    pattern: _re.Pattern = _dc.field(init=False)
    regex: _dc.InitVar[str]

    # For tokens with "overlapping" patterns, the one with the higher priority
    # will be tried to match first
    priority: int = -1

    def __post_init__(self, regex: str) -> None:
        self.pattern = _re.compile(regex)


END_TOKEN = TokenDefinition("END", r"$")


@_dc.dataclass
class Token:
    definition: TokenDefinition
    value: str
    input_string: str
    start_index: int
    end_index: int


LexerResult = Token | ParsingError


@_dc.dataclass
class ParsingErrorException(Exception):
    parsing_error: ParsingError


_WHITESPACE = _re.compile(r"[ \t]+")


class Lexer:
    def __init__(self, input_string: str, token_definitions: _tp.Sequence[TokenDefinition]) -> None:
        self._input_string = input_string

        def get_priority(token_definition: TokenDefinition) -> int:
            return token_definition.priority

        self._token_definitions = [*sorted(token_definitions, key=get_priority), END_TOKEN]
        self._current_pos = 0

    def get_next_token(self) -> LexerResult:
        match = _WHITESPACE.match(self._input_string)
        if match:
            self._advance_input(match.end())

        for token_definition in self._token_definitions:
            match = token_definition.pattern.match(self._input_string, pos=self._current_pos)
            if match:
                self._advance_input(match.end())
                token_definition = Token(
                    token_definition, match.group(), self._input_string, match.start(), match.end()
                )
                return token_definition

        parsing_error = ParsingError(
            "Not a recognized token.",
            self._input_string,
            self._current_pos,
        )

        return parsing_error

    def _advance_input(self, to: int) -> None:
        self._current_pos = to


class ParserBase(_tp.Generic[_TCo], _abc.ABC):
    def __int__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: _tp.Optional[Token]

    def _accept(self, token_definition: TokenDefinition) -> str | None:
        if self._current_token.definition != token_definition:
            return None

        value = self._current_token.value

        self._set_next_token()

        return value

    def _expect(self, token_definition: TokenDefinition) -> str:
        value = self._accept(token_definition)
        if value:
            return value

        expected_token = token_definition.name
        actual_token = self._current_token.definition.name

        parsing_error = ParsingError(
            f"Expected {expected_token} but found {actual_token}.",
            self._current_token.input_string,
            self._current_token.start_index,
        )

        raise ParsingErrorException(parsing_error)

    def _set_next_token(self) -> None:
        next_token = self._lexer.get_next_token()
        if isinstance(next_token, ParsingError):
            raise ParsingErrorException(next_token)
        self._current_token = next_token

    @_abc.abstractmethod
    def parse(self) -> ParserResult[_TCo]:
        raise NotImplementedError()
