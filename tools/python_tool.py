import ast
import math


class PythonTool:

    name = "python"

    description = (
        "Safely executes a restricted subset of Python "
        "expressions and simple statements."
    )

    MAX_SOURCE_LENGTH = 2000

    ALLOWED_BUILTINS = {
        "abs": abs,
        "bool": bool,
        "float": float,
        "int": int,
        "len": len,
        "max": max,
        "min": min,
        "round": round,
        "sum": sum,
    }

    ALLOWED_MATH = {
        name: getattr(math, name)
        for name in {
            "ceil",
            "floor",
            "sqrt",
            "sin",
            "cos",
            "tan",
            "log",
            "log10",
            "exp",
            "factorial",
            "pi",
            "e",
        }
    }

    ALLOWED_BINARY_OPERATORS = {
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
    }

    ALLOWED_UNARY_OPERATORS = {
        ast.UAdd,
        ast.USub,
        ast.Not,
    }

    ALLOWED_COMPARISON_OPERATORS = {
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
        ast.In,
        ast.NotIn,
        ast.Is,
        ast.IsNot,
    }

    ALLOWED_NODES = {
        ast.Module,
        ast.Expr,
        ast.Assign,
        ast.Name,
        ast.Load,
        ast.Store,
        ast.Constant,
        ast.List,
        ast.Tuple,
        ast.Set,
        ast.Dict,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,
        ast.IfExp,
        ast.Subscript,
        ast.Slice,
        ast.Attribute,
    }

    BLOCKED_NAMES = {
        "__import__",
        "__builtins__",
        "eval",
        "exec",
        "compile",
        "open",
        "input",
        "globals",
        "locals",
        "vars",
        "dir",
        "getattr",
        "setattr",
        "delattr",
        "help",
        "breakpoint",
        "memoryview",
        "type",
        "object",
        "super",
    }

    BLOCKED_ATTRIBUTES = {
        "__class__",
        "__bases__",
        "__base__",
        "__subclasses__",
        "__mro__",
        "__globals__",
        "__code__",
        "__closure__",
        "__func__",
        "__self__",
        "__dict__",
        "__module__",
    }

    def execute(self, source):

        if source is None:

            raise ValueError(
                "Python source cannot be empty."
            )

        source = str(source).strip()

        if not source:

            raise ValueError(
                "Python source cannot be empty."
            )

        if len(source) > self.MAX_SOURCE_LENGTH:

            raise ValueError(
                "Python source is too long."
            )

        try:

            tree = ast.parse(
                source,
                mode="exec"
            )

        except SyntaxError as error:

            raise ValueError(
                "Invalid Python syntax."
            ) from error

        self._validate_tree(tree)

        namespace = {
            "__builtins__": dict(
                self.ALLOWED_BUILTINS
            ),
            "math": _SafeMath(),
        }

        output = []

        namespace["print"] = (
            lambda *args, **kwargs:
            output.append(
                " ".join(
                    str(value)
                    for value in args
                )
            )
        )

        try:

            self._execute_statements(
                tree.body,
                namespace
            )

        except (
            ValueError,
            TypeError,
            ZeroDivisionError,
            OverflowError,
            ArithmeticError
        ) as error:

            raise ValueError(
                str(error)
            ) from error

        return {
            "result": namespace.get(
                "_"
            ),
            "output": "\n".join(output)
        }

    def _validate_tree(self, tree):

        for node in ast.walk(tree):

            if type(node) not in self.ALLOWED_NODES:

                raise ValueError(
                    "Python operation is not allowed: "
                    f"{type(node).__name__}"
                )

            if isinstance(
                node,
                ast.Name
            ):

                if node.id in self.BLOCKED_NAMES:

                    raise ValueError(
                        f"Python name is blocked: {node.id}"
                    )

            if isinstance(
                node,
                ast.Attribute
            ):

                if node.attr in self.BLOCKED_ATTRIBUTES:

                    raise ValueError(
                        "Access to this Python attribute "
                        "is blocked."
                    )

                if node.attr.startswith("__"):

                    raise ValueError(
                        "Private Python attributes "
                        "are blocked."
                    )

            if isinstance(
                node,
                ast.Call
            ):

                if isinstance(
                    node.func,
                    ast.Name
                ):

                    if node.func.id in self.BLOCKED_NAMES:

                        raise ValueError(
                            "Blocked function call."
                        )

    def _execute_statements(
        self,
        statements,
        namespace
    ):

        for statement in statements:

            if isinstance(
                statement,
                ast.Expr
            ):

                value = self._evaluate(
                    statement.value,
                    namespace
                )

                namespace["_"] = value

            elif isinstance(
                statement,
                ast.Assign
            ):

                value = self._evaluate(
                    statement.value,
                    namespace
                )

                for target in statement.targets:

                    if not isinstance(
                        target,
                        ast.Name
                    ):

                        raise ValueError(
                            "Only simple variable "
                            "assignment is allowed."
                        )

                    if target.id.startswith("_"):

                        raise ValueError(
                            "Private variable names "
                            "are not allowed."
                        )

                    namespace[target.id] = value

                namespace["_"] = value

            else:

                raise ValueError(
                    "Python statement is not allowed."
                )

    def _evaluate(
        self,
        node,
        namespace
    ):

        if isinstance(
            node,
            ast.Constant
        ):

            if isinstance(
                node.value,
                (str, int, float, bool, type(None))
            ):

                return node.value

            raise ValueError(
                "Constant type is not allowed."
            )

        if isinstance(
            node,
            ast.Name
        ):

            if node.id in namespace:

                return namespace[node.id]

            raise ValueError(
                f"Unknown variable: {node.id}"
            )

        if isinstance(
            node,
            ast.List
        ):

            return [
                self._evaluate(
                    element,
                    namespace
                )
                for element in node.elts
            ]

        if isinstance(
            node,
            ast.Tuple
        ):

            return tuple(
                self._evaluate(
                    element,
                    namespace
                )
                for element in node.elts
            )

        if isinstance(
            node,
            ast.Set
        ):

            return {
                self._evaluate(
                    element,
                    namespace
                )
                for element in node.elts
            }

        if isinstance(
            node,
            ast.Dict
        ):

            return {
                self._evaluate(
                    key,
                    namespace
                ):
                self._evaluate(
                    value,
                    namespace
                )
                for key, value
                in zip(
                    node.keys,
                    node.values
                )
            }

        if isinstance(
            node,
            ast.BinOp
        ):

            if type(node.op) not in (
                self.ALLOWED_BINARY_OPERATORS
            ):

                raise ValueError(
                    "Binary operator is not allowed."
                )

            left = self._evaluate(
                node.left,
                namespace
            )

            right = self._evaluate(
                node.right,
                namespace
            )

            return self._binary_operation(
                node.op,
                left,
                right
            )

        if isinstance(
            node,
            ast.UnaryOp
        ):

            if type(node.op) not in (
                self.ALLOWED_UNARY_OPERATORS
            ):

                raise ValueError(
                    "Unary operator is not allowed."
                )

            value = self._evaluate(
                node.operand,
                namespace
            )

            if isinstance(
                node.op,
                ast.UAdd
            ):

                return +value

            if isinstance(
                node.op,
                ast.USub
            ):

                return -value

            if isinstance(
                node.op,
                ast.Not
            ):

                return not value

        if isinstance(
            node,
            ast.BoolOp
        ):

            values = [
                self._evaluate(
                    value,
                    namespace
                )
                for value in node.values
            ]

            if isinstance(
                node.op,
                ast.And
            ):

                return all(values)

            if isinstance(
                node.op,
                ast.Or
            ):

                return any(values)

            raise ValueError(
                "Boolean operator is not allowed."
            )

        if isinstance(
            node,
            ast.Compare
        ):

            left = self._evaluate(
                node.left,
                namespace
            )

            for operator_node, comparator in zip(
                node.ops,
                node.comparators
            ):

                if type(
                    operator_node
                ) not in self.ALLOWED_COMPARISON_OPERATORS:

                    raise ValueError(
                        "Comparison operator is not allowed."
                    )

                right = self._evaluate(
                    comparator,
                    namespace
                )

                if not self._compare(
                    operator_node,
                    left,
                    right
                ):

                    return False

                left = right

            return True

        if isinstance(
            node,
            ast.IfExp
        ):

            condition = self._evaluate(
                node.test,
                namespace
            )

            if condition:

                return self._evaluate(
                    node.body,
                    namespace
                )

            return self._evaluate(
                node.orelse,
                namespace
            )

        if isinstance(
            node,
            ast.Call
        ):

            function = self._evaluate(
                node.func,
                namespace
            )

            arguments = [
                self._evaluate(
                    argument,
                    namespace
                )
                for argument in node.args
            ]

            return function(*arguments)

        if isinstance(
            node,
            ast.Attribute
        ):

            value = self._evaluate(
                node.value,
                namespace
            )

            if node.attr.startswith("_"):

                raise ValueError(
                    "Private attributes are blocked."
                )

            if not isinstance(
                value,
                _SafeMath
            ):

                raise ValueError(
                    "Attribute access is restricted."
                )

            if node.attr not in self.ALLOWED_MATH:

                raise ValueError(
                    "Math function is not allowed."
                )

            return self.ALLOWED_MATH[
                node.attr
            ]

        if isinstance(
            node,
            ast.Subscript
        ):

            value = self._evaluate(
                node.value,
                namespace
            )

            index = self._evaluate(
                node.slice,
                namespace
            )

            return value[index]

        if isinstance(
            node,
            ast.Slice
        ):

            lower = (
                self._evaluate(
                    node.lower,
                    namespace
                )
                if node.lower
                else None
            )

            upper = (
                self._evaluate(
                    node.upper,
                    namespace
                )
                if node.upper
                else None
            )

            step = (
                self._evaluate(
                    node.step,
                    namespace
                )
                if node.step
                else None
            )

            return slice(
                lower,
                upper,
                step
            )

        raise ValueError(
            "Python expression is not allowed."
        )

    @staticmethod
    def _binary_operation(
        operator_node,
        left,
        right
    ):

        if isinstance(
            operator_node,
            ast.Add
        ):
            return left + right

        if isinstance(
            operator_node,
            ast.Sub
        ):
            return left - right

        if isinstance(
            operator_node,
            ast.Mult
        ):
            return left * right

        if isinstance(
            operator_node,
            ast.Div
        ):
            return left / right

        if isinstance(
            operator_node,
            ast.FloorDiv
        ):
            return left // right

        if isinstance(
            operator_node,
            ast.Mod
        ):
            return left % right

        if isinstance(
            operator_node,
            ast.Pow
        ):

            if abs(right) > 1000:

                raise ValueError(
                    "Exponent is too large."
                )

            return left ** right

        raise ValueError(
            "Binary operator is not allowed."
        )

    @staticmethod
    def _compare(
        operator_node,
        left,
        right
    ):

        if isinstance(
            operator_node,
            ast.Eq
        ):
            return left == right

        if isinstance(
            operator_node,
            ast.NotEq
        ):
            return left != right

        if isinstance(
            operator_node,
            ast.Lt
        ):
            return left < right

        if isinstance(
            operator_node,
            ast.LtE
        ):
            return left <= right

        if isinstance(
            operator_node,
            ast.Gt
        ):
            return left > right

        if isinstance(
            operator_node,
            ast.GtE
        ):
            return left >= right

        if isinstance(
            operator_node,
            ast.In
        ):
            return left in right

        if isinstance(
            operator_node,
            ast.NotIn
        ):
            return left not in right

        if isinstance(
            operator_node,
            ast.Is
        ):
            return left is right

        if isinstance(
            operator_node,
            ast.IsNot
        ):
            return left is not right

        raise ValueError(
            "Comparison operator is not allowed."
        )


class _SafeMath:

    pass