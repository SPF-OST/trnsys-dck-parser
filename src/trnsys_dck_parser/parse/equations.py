import typing as _tp
import re as _re

import trnsys_dck_parser.model.equations as _meqs
import trnsys_dck_parser.model.expression as _mexp
import trnsys_dck_parser.parse.common as _pcom
import trnsys_dck_parser.parse.tokens as _ptok
import trnsys_dck_parser.parse.expression.parse as _pexp


class Tokens:
    EQUATIONS = _pcom.TokenDefinition("EQUATIONS", r"EQUATIONS", _re.RegexFlag.IGNORECASE)
    POSITIVE_INTEGER = _pcom.TokenDefinition("positive integer", _ptok.Regexes.POSITIVE_INTEGER)
    EQUALS = _pcom.TokenDefinition("=", r"=")


class Parser(_pcom.ParserBase[_meqs.Equations]):
    def __init__(self, input_string: str, start_pos: int = 0) -> None:
        lexer = _pcom.Lexer(
            input_string, [Tokens.EQUATIONS, Tokens.POSITIVE_INTEGER, Tokens.EQUALS, _ptok.Tokens.IDENTIFIER], start_pos
        )
        super().__init__(lexer)

    def parse(self) -> _pcom.ParseResult[_meqs.Equations]:
        try:
            equations = self._equations()
            return _pcom.ParseSuccess(equations, self._remaining_input_string_start_index)
        except _pcom.ParseErrorException as exception:
            return exception.parse_error

    def _equations(self) -> _meqs.Equations:
        self._expect(Tokens.EQUATIONS)

        n_equations_value = self._expect(Tokens.POSITIVE_INTEGER)
        n_equations = None if n_equations_value is None else int(n_equations_value)

        equations = [self._equation()]
        while True:
            try:
                equations.append(self._equation())
            except _pcom.ParseErrorException:
                break

        return _meqs.Equations(n_equations, equations)

    def _equation(self) -> _meqs.Equation:
        variable_name = self._expect(_ptok.Tokens.IDENTIFIER)
        self._expect(Tokens.EQUALS)
        expression = self._expression()
        equation = _meqs.Equation(variable_name, expression)
        return equation

    def _expression(self) -> _mexp.Expression:
        parser = _pexp.Parser(self._lexer.input_string, self._remaining_input_string_start_index)
        return self._expect_sub_parser(parser)


def parse_equations(input_string: str) -> _pcom.ParseResult[_meqs.Equations]:
    parser = Parser(input_string)
    return parser.parse()
