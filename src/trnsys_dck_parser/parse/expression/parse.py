import dataclasses as _dc
import typing as _tp

import trnsys_dck_parser.model.expression as _exp
import trnsys_dck_parser.parse.common as _pcom
import trnsys_dck_parser.parse.expression.tokenize as _petok
import trnsys_dck_parser.parse.tokens as _ptok


@_dc.dataclass
class ExpressionWithRemainingStartIndex:
    expression: _exp.Expression
    remaining_input_string_start_index: int


ParseResult = _pcom.ParseResult[_exp.Expression]


class Parser(_pcom.ParserBase[_exp.Expression]):
    def __init__(self, input_string: str, start_pos: int = 0) -> None:
        lexer = _petok.create_lexer(input_string, start_pos)
        super().__init__(lexer)

    def parse(self) -> ParseResult:
        try:
            expression = self._expression()
            parse_success = _pcom.ParseSuccess(expression, self._remaining_input_string_start_index)
            return parse_success
        except _pcom.ParseErrorException as exception:
            return exception.parse_error

    def _expression(self) -> _exp.Expression:
        addend = self._addend()
        while True:
            if self._accept(_petok.Tokens.PLUS):
                next_addend = self._addend()
                addend += next_addend
            elif self._accept(_petok.Tokens.MINUS):
                next_addend = self._addend()
                addend -= next_addend
            else:
                break

        return addend

    def _addend(self) -> _exp.Expression:
        multiplicand = self._multiplicand()
        while True:
            if self._accept(_petok.Tokens.TIMES):
                next_multiplicand = self._multiplicand()
                multiplicand *= next_multiplicand
            elif self._accept(_petok.Tokens.DIVIDE):
                next_multiplicand = self._multiplicand()
                multiplicand /= next_multiplicand
            else:
                break

        return multiplicand

    def _multiplicand(self) -> _exp.Expression:
        base = self._power_operand()

        if not self._accept(_petok.Tokens.POWER):
            return base

        exponent = self._power_operand()

        return base ** exponent

    def _power_operand(self) -> _exp.Expression:  # pylint: disable=too-many-return-statements
        if positive_integer := self._accept(_petok.Tokens.POSITIVE_INTEGER):
            return _exp.Literal(int(positive_integer))

        if negative_integer := self._accept(_petok.Tokens.NEGATIVE_INTEGER):
            return _exp.Literal(int(negative_integer))

        if number := self._accept(_petok.Tokens.FLOAT):
            return _exp.Literal(float(number))

        if identifier := self._accept(_ptok.Tokens.IDENTIFIER):
            if not self._accept(_petok.Tokens.LEFT_PAREN):
                return _exp.Variable(identifier)

            arguments = self._argument_list()
            self._expect(_petok.Tokens.RIGHT_PAREN)
            return _exp.FunctionCall(identifier, arguments)

        if self._accept(_petok.Tokens.LEFT_SQUARE_BRACKET):
            unit_number, output_number = self._unit_and_output_number()
            self._expect(_petok.Tokens.RIGHT_SQUARE_BRACKET)
            return _exp.UnitOutput(unit_number, output_number)

        if self._accept(_petok.Tokens.MINUS):
            return -self._expression()

        if self._accept(_petok.Tokens.LEFT_PAREN):
            expression = self._expression()
            self._expect(_petok.Tokens.RIGHT_PAREN)
            return expression

        self._raise_parsing_error(
            "Expected number, variable, function call, opening square bracket or "
            "opening parenthesis but found {actual_token}"
        )

    def _argument_list(self) -> _tp.Sequence[_exp.Expression]:
        arguments = [self._expression()]
        while self._accept(_petok.Tokens.COMMA):
            argument = self._expression()
            arguments.append(argument)

        return arguments

    def _unit_and_output_number(self) -> _tp.Tuple[int, int]:
        unit_number = int(self._expect(_petok.Tokens.POSITIVE_INTEGER))

        self._expect(_petok.Tokens.COMMA)

        output_number = int(self._expect(_petok.Tokens.POSITIVE_INTEGER))

        return unit_number, output_number
