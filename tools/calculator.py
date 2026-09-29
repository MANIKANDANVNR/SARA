import ast
import operator


class CalculatorTool:

    name = "calculator"

    description = (
        "Safely evaluates basic mathematical expressions."
    )

    _OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    def execute(self, expression):

        if expression is None:

            raise ValueError(
                "Expression cannot be empty."
            )

        expression = str(
            expression
        ).strip()

        if not expression:

            raise ValueError(
                "Expression cannot be empty."
            )

        try:

            tree = ast.parse(
                expression,
                mode="eval"
            )

        except SyntaxError as error:

            raise ValueError(
                "Invalid mathematical expression."
            ) from error

        return self._evaluate(
            tree.body
        )

    def _evaluate(self, node):

        if isinstance(
            node,
            ast.Constant
        ):

            if isinstance(
                node.value,
                bool
            ):

                raise ValueError(
                    "Boolean values are not allowed."
                )

            if isinstance(
                node.value,
                (int, float)
            ):

                return node.value

            raise ValueError(
                "Only numeric values are allowed."
            )

        if isinstance(
            node,
            ast.BinOp
        ):

            operator_function = (
                self._OPERATORS.get(
                    type(node.op)
                )
            )

            if operator_function is None:

                raise ValueError(
                    "Operator is not allowed."
                )

            left = self._evaluate(
                node.left
            )

            right = self._evaluate(
                node.right
            )

            try:

                return operator_function(
                    left,
                    right
                )

            except (
                ZeroDivisionError,
                OverflowError
            ) as error:

                raise ValueError(
                    str(error)
                ) from error

        if isinstance(
            node,
            ast.UnaryOp
        ):

            operator_function = (
                self._OPERATORS.get(
                    type(node.op)
                )
            )

            if operator_function is None:

                raise ValueError(
                    "Unary operator is not allowed."
                )

            value = self._evaluate(
                node.operand
            )

            return operator_function(
                value
            )

        raise ValueError(
            "Expression contains an unsupported operation."
        )