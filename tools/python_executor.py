import ast
import operator


class PythonExecutorTool:

    name = "python"

    description = (
        "Safely executes a restricted subset of Python code."
    )

    MAX_CODE_LENGTH = 5000

    MAX_LOOP_ITERATIONS = 1000

    MAX_OUTPUT_LENGTH = 10000

    BINARY_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow
    }

    COMPARISON_OPERATORS = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge
    }

    UNARY_OPERATORS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
        ast.Not: operator.not_
    }

    ALLOWED_BUILTINS = {
        "abs": abs,
        "min": min,
        "max": max,
        "round": round,
        "len": len,
        "sum": sum
    }

    def __init__(self):

        self.variables = {}

        self.output = []

        self.loop_iterations = 0

    # =================================================
    # PUBLIC EXECUTION
    # =================================================

    def execute(self, code):

        if code is None:

            raise ValueError(
                "Python code cannot be empty."
            )

        code = str(code).strip()

        if not code:

            raise ValueError(
                "Python code cannot be empty."
            )

        if len(code) > self.MAX_CODE_LENGTH:

            raise ValueError(
                "Python code is too long."
            )

        self.variables = {}

        self.output = []

        self.loop_iterations = 0

        try:

            tree = ast.parse(
                code,
                mode="exec"
            )

        except SyntaxError as error:

            raise ValueError(
                "Invalid Python syntax."
            ) from error

        self._validate_tree(tree)

        result = self._execute_statements(
            tree.body
        )

        if self.output:

            output = "\n".join(
                self.output
            )

            if len(output) > self.MAX_OUTPUT_LENGTH:

                output = output[
                    :self.MAX_OUTPUT_LENGTH
                ]

                output += (
                    "\n[Output truncated.]"
                )

            return output

        if result is not None:

            return result

        return None

    # =================================================
    # AST VALIDATION
    # =================================================

    def _validate_tree(self, tree):

        for node in ast.walk(tree):

            if isinstance(
                node,
                (
                    ast.Import,
                    ast.ImportFrom,
                    ast.With,
                    ast.AsyncWith,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                    ast.Lambda,
                    ast.Try,
                    ast.Raise,
                    ast.Delete,
                    ast.Global,
                    ast.Nonlocal,
                    ast.Yield,
                    ast.YieldFrom,
                    ast.Await
                )
            ):

                raise ValueError(
                    f"Python operation is not allowed: "
                    f"{type(node).__name__}"
                )

            if isinstance(
                node,
                ast.Attribute
            ):

                raise ValueError(
                    "Attribute access is not allowed."
                )

            if isinstance(
                node,
                ast.Starred
            ):

                raise ValueError(
                    "Starred expressions are not allowed."
                )

            if isinstance(
                node,
                ast.NamedExpr
            ):

                raise ValueError(
                    "Assignment expressions are not allowed."
                )

            if isinstance(
                node,
                ast.comprehension
            ):

                raise ValueError(
                    "Comprehensions are not allowed."
                )

    # =================================================
    # STATEMENT EXECUTION
    # =================================================

    def _execute_statements(
        self,
        statements
    ):

        result = None

        for statement in statements:

            result = self._execute_statement(
                statement
            )

        return result

    def _execute_statement(
        self,
        statement
    ):

        if isinstance(
            statement,
            ast.Assign
        ):

            value = self._evaluate(
                statement.value
            )

            for target in statement.targets:

                self._assign(
                    target,
                    value
                )

            return value

        if isinstance(
            statement,
            ast.AnnAssign
        ):

            if statement.value is None:

                raise ValueError(
                    "Variable declaration requires a value."
                )

            value = self._evaluate(
                statement.value
            )

            self._assign(
                statement.target,
                value
            )

            return value

        if isinstance(
            statement,
            ast.Expr
        ):

            return self._evaluate(
                statement.value
            )

        if isinstance(
            statement,
            ast.If
        ):

            condition = self._evaluate(
                statement.test
            )

            if condition:

                return self._execute_statements(
                    statement.body
                )

            return self._execute_statements(
                statement.orelse
            )

        if isinstance(
            statement,
            ast.For
        ):

            return self._execute_for(
                statement
            )

        if isinstance(
            statement,
            ast.Pass
        ):

            return None

        raise ValueError(
            f"Python statement is not allowed: "
            f"{type(statement).__name__}"
        )

    # =================================================
    # FOR LOOP
    # =================================================

    def _execute_for(
        self,
        statement
    ):

        iterable = self._evaluate(
            statement.iter
        )

        if not isinstance(
            iterable,
            range
        ):

            raise ValueError(
                "Only range() is allowed in for loops."
            )

        result = None

        for value in iterable:

            self.loop_iterations += 1

            if (
                self.loop_iterations
                > self.MAX_LOOP_ITERATIONS
            ):

                raise ValueError(
                    "Maximum loop iteration limit exceeded."
                )

            self._assign(
                statement.target,
                value
            )

            result = self._execute_statements(
                statement.body
            )

        if statement.orelse:

            result = self._execute_statements(
                statement.orelse
            )

        return result

    # =================================================
    # ASSIGNMENT
    # =================================================

    def _assign(
        self,
        target,
        value
    ):

        if isinstance(
            target,
            ast.Name
        ):

            self.variables[
                target.id
            ] = value

            return

        raise ValueError(
            "Only simple variable assignment is allowed."
        )

    # =================================================
    # EXPRESSION EVALUATION
    # =================================================

    def _evaluate(
        self,
        node
    ):

        if isinstance(
            node,
            ast.Constant
        ):

            if isinstance(
                node.value,
                (
                    str,
                    int,
                    float,
                    bool,
                    type(None)
                )
            ):

                return node.value

            raise ValueError(
                "This constant type is not allowed."
            )

        if isinstance(
            node,
            ast.Name
        ):

            if node.id in self.variables:

                return self.variables[
                    node.id
                ]

            if node.id in {
                "True",
                "False",
                "None"
            }:

                return {
                    "True": True,
                    "False": False,
                    "None": None
                }[node.id]

            raise ValueError(
                f"Unknown variable: {node.id}"
            )

        if isinstance(
            node,
            ast.BinOp
        ):

            function = self.BINARY_OPERATORS.get(
                type(node.op)
            )

            if function is None:

                raise ValueError(
                    "Binary operator is not allowed."
                )

            left = self._evaluate(
                node.left
            )

            right = self._evaluate(
                node.right
            )

            try:

                return function(
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

            function = self.UNARY_OPERATORS.get(
                type(node.op)
            )

            if function is None:

                raise ValueError(
                    "Unary operator is not allowed."
                )

            value = self._evaluate(
                node.operand
            )

            return function(
                value
            )

        if isinstance(
            node,
            ast.BoolOp
        ):

            if isinstance(
                node.op,
                ast.And
            ):

                result = True

                for value_node in node.values:

                    result = self._evaluate(
                        value_node
                    )

                    if not result:

                        return result

                return result

            if isinstance(
                node.op,
                ast.Or
            ):

                result = False

                for value_node in node.values:

                    result = self._evaluate(
                        value_node
                    )

                    if result:

                        return result

                return result

            raise ValueError(
                "Boolean operator is not allowed."
            )

        if isinstance(
            node,
            ast.Compare
        ):

            left = self._evaluate(
                node.left
            )

            for operator_node, comparator in zip(
                node.ops,
                node.comparators
            ):

                function = (
                    self.COMPARISON_OPERATORS.get(
                        type(operator_node)
                    )
                )

                if function is None:

                    raise ValueError(
                        "Comparison operator is not allowed."
                    )

                right = self._evaluate(
                    comparator
                )

                if not function(
                    left,
                    right
                ):

                    return False

                left = right

            return True

        if isinstance(
            node,
            ast.Call
        ):

            return self._evaluate_call(
                node
            )

        if isinstance(
            node,
            ast.List
        ):

            return [
                self._evaluate(element)
                for element in node.elts
            ]

        if isinstance(
            node,
            ast.Tuple
        ):

            return tuple(
                self._evaluate(element)
                for element in node.elts
            )

        if isinstance(
            node,
            ast.Set
        ):

            return {
                self._evaluate(element)
                for element in node.elts
            }

        raise ValueError(
            f"Python expression is not allowed: "
            f"{type(node).__name__}"
        )

    # =================================================
    # FUNCTION CALLS
    # =================================================

    def _evaluate_call(
        self,
        node
    ):

        if not isinstance(
            node.func,
            ast.Name
        ):

            raise ValueError(
                "Only approved functions can be called."
            )

        function_name = node.func.id

        if function_name == "print":

            values = [
                self._evaluate(argument)
                for argument in node.args
            ]

            if node.keywords:

                raise ValueError(
                    "Keyword arguments are not allowed."
                )

            text = " ".join(
                str(value)
                for value in values
            )

            self.output.append(
                text
            )

            return None

        if function_name == "range":

            if node.keywords:

                raise ValueError(
                    "Keyword arguments are not allowed."
                )

            arguments = [
                self._evaluate(argument)
                for argument in node.args
            ]

            if not 1 <= len(arguments) <= 3:

                raise ValueError(
                    "range() requires one to three arguments."
                )

            if not all(
                isinstance(
                    value,
                    int
                )
                and not isinstance(
                    value,
                    bool
                )
                for value in arguments
            ):

                raise ValueError(
                    "range() arguments must be integers."
                )

            result = range(
                *arguments
            )

            if len(result) > self.MAX_LOOP_ITERATIONS:

                raise ValueError(
                    "range() exceeds the loop iteration limit."
                )

            return result

        function = self.ALLOWED_BUILTINS.get(
            function_name
        )

        if function is None:

            raise ValueError(
                f"Function '{function_name}' is not allowed."
            )

        if node.keywords:

            raise ValueError(
                "Keyword arguments are not allowed."
            )

        arguments = [
            self._evaluate(argument)
            for argument in node.args
        ]

        try:

            return function(
                *arguments
            )

        except Exception as error:

            raise ValueError(
                str(error)
            ) from error