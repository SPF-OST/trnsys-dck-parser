import dataclasses as _dc
import typing as _tp

import trnsys_dck_parser.model.expression as _exp

from .. import common as _com

from . import tokenize as _tok


@_dc.dataclass
class ExpressionWithRemainingStartIndex:
    expression: _exp.Expression
    remaining_input_string_start_index: int


class Parser(_com.ParserBase[_exp.Expression]):
    def __init__(self, input_string: str) -> None:
        lexer = _tok.create_lexer(input_string)
        super().__int__(lexer)

    def parse(self) -> _com.ParserResult:
        self._set_next_token()
        try:
            expression = self._expression()
            parseSuccess = _com.ParseSuccess(expression, self._remaining_input_string_start_index)
            return parseSuccess
        except _com.ParsingErrorException as exception:
            return exception.parsing_error

    def _expression(self) -> _exp.Expression:
        addend = self._addend()
        while True:
            if self._accept(_tok.Tokens.PLUS):
                next_addend = self._addend()
                addend += next_addend
            elif self._accept(_tok.Tokens.MINUS):
                next_addend = self._addend()
                addend -= next_addend
            else:
                break

        return addend

    def _addend(self) -> _exp.Expression:
        multiplicand = self._multiplicand()
        while True:
            if self._accept(_tok.Tokens.TIMES):
                next_multiplicand = self._multiplicand()
                multiplicand *= next_multiplicand
            elif self._accept(_tok.Tokens.DIVIDE):
                next_multiplicand = self._multiplicand()
                multiplicand /= next_multiplicand
            else:
                break

        return multiplicand

    def _multiplicand(self) -> _exp.Expression:
        base = self._power_operand()

        if not self._accept(_tok.Tokens.POWER):
            return base

        exponent = self._power_operand()

        return base**exponent

    def _power_operand(self) -> _exp.Expression:
        if integer := self._accept(_tok.Tokens.INTEGER):
            return _exp.Literal(int(integer))

        if number := self._accept(_tok.Tokens.FLOAT):
            return _exp.Literal(float(number))

        if identifier := self._accept(_tok.Tokens.IDENTIFIER):
            if not self._accept(_tok.Tokens.LEFT_PAREN):
                return _exp.Variable(identifier)

            arguments = self._argument_list()
            self._expect(_tok.Tokens.RIGHT_PAREN)
            return _exp.FunctionCall(identifier, *arguments)

        if self._accept(_tok.Tokens.LEFT_SQUARE_BRACKET):
            unit_number, output_number = self._unit_and_output_number()
            self._expect(_tok.Tokens.RIGHT_SQUARE_BRACKET)
            return _exp.UnitOutput(unit_number, output_number)

        if self._accept(_tok.Tokens.MINUS):
            return -self._expression()

        if self._accept(_tok.Tokens.LEFT_PAREN):
            expression = self._expression()
            self._expect(_tok.Tokens.RIGHT_PAREN)
            return expression

        self._raise_parsing_error(
            "Expected number, variable, function call, opening square bracket or "
            "opening parenthesis but found {actual_token}"
        )

    def _argument_list(self) -> _tp.Sequence[_exp.Expression]:
        arguments = [self._expression()]
        while self._accept(_tok.Tokens.COMMA):
            argument = self._expression()
            arguments.append(argument)

        return arguments

    def _unit_and_output_number(self) -> _tp.Tuple[int, int]:
        self._expect(_tok.Tokens.INTEGER)
        unit_number = int(self._current_token.value)
        self._check_non_negative(unit_number)

        self._expect(_tok.Tokens.COMMA)

        self._expect(_tok.Tokens.INTEGER)
        output_number = int(self._current_token.value)
        self._check_non_negative(unit_number)

        return unit_number, output_number

    def _check_non_negative(self, integer):
        if integer >= 0:
            return

        self._raise_parsing_error("Unit numbers must be non-negative.")
