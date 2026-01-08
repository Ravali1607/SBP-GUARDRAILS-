# validator/cucumber_validator.py
from cucumber_expressions.parameter_type import ParameterType
from cucumber_expressions.expression import CucumberExpression
from cucumber_expressions.parameter_type_registry import ParameterTypeRegistry
import rstr
from guardrails.validator_base import FailResult, PassResult, ValidationResult

class CucumberValidator:
    def __init__(self, expressions=None, parameter_types=None):
        self._expressions = expressions or []
        self._parameter_type_registry = ParameterTypeRegistry()
        parameter_types = parameter_types or []
        for pt in parameter_types:
            self._parameter_type_registry.define_parameter_type(pt)
    def validate(self, value: str):
        """
        Pass if ANY cucumber expression matches
        """
        for expr in self._expressions:
            cucumber_expr = CucumberExpression(expr, self._parameter_type_registry)
            matched = cucumber_expr.match(value)

            if matched is not None:
                return {
                    "passed": True,
                    "message": f"Matched expression: {expr}"
                }

        # If none matched
        return {
            "passed": False,
            "message": "Text does not match any allowed cucumber expressions"
        }

    # def validate(self, value: str):
    #     """Validate text against cucumber-expression."""
    #     this_expression = CucumberExpression(self._expression, self._parameter_type_registry)
    #     matched = this_expression.match(value)
    #     if matched is None:
    #         fix_string = rstr.xeger(this_expression.regexp)
    #         return {
    #             # "status": "error",
    #             "message": f"Result must match: {self._expression}",
    #             # "suggested_fix": fix_string,
    #             "passed": False
    #         }

    #     return {
    #         # "status": "success",
    #         "message": "Text matches cucumber-expression",
    #         "passed": True
    #     }
