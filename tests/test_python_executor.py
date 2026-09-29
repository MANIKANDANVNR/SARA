import pytest

from tools.python_executor import (
    PythonExecutorTool
)


def test_python_executor_has_correct_name():

    tool = PythonExecutorTool()

    assert tool.name == "python"


def test_python_executor_has_description():

    tool = PythonExecutorTool()

    assert tool.description


def test_simple_expression():

    tool = PythonExecutorTool()

    result = tool.execute(
        "10 + 20"
    )

    assert result == 30


def test_variable_assignment():

    tool = PythonExecutorTool()

    result = tool.execute(
        """
x = 10
x * 5
"""
    )

    assert result == 50


def test_multiple_variables():

    tool = PythonExecutorTool()

    result = tool.execute(
        """
x = 10
y = 20
x + y
"""
    )

    assert result == 30


def test_print():

    tool = PythonExecutorTool()

    result = tool.execute(
        'print("Hello SARA")'
    )

    assert result == "Hello SARA"


def test_multiple_prints():

    tool = PythonExecutorTool()

    result = tool.execute(
        """
print("Hello")
print("SARA")
"""
    )

    assert result == "Hello\nSARA"


def test_if_statement():

    tool = PythonExecutorTool()

    result = tool.execute(
        """
x = 10

if x > 5:
    print("greater")
"""
    )

    assert result == "greater"


def test_for_range():

    tool = PythonExecutorTool()

    result = tool.execute(
        """
for i in range(3):
    print(i)
"""
    )

    assert result == "0\n1\n2"


def test_allowed_builtin_abs():

    tool = PythonExecutorTool()

    result = tool.execute(
        "abs(-10)"
    )

    assert result == 10


def test_allowed_builtin_len():

    tool = PythonExecutorTool()

    result = tool.execute(
        'len("SARA")'
    )

    assert result == 4


def test_allowed_builtin_sum():

    tool = PythonExecutorTool()

    result = tool.execute(
        "sum([1, 2, 3, 4])"
    )

    assert result == 10


def test_boolean_comparison():

    tool = PythonExecutorTool()

    result = tool.execute(
        "10 > 5"
    )

    assert result is True


def test_boolean_logic():

    tool = PythonExecutorTool()

    result = tool.execute(
        "10 > 5 and 20 > 10"
    )

    assert result is True


def test_lists():

    tool = PythonExecutorTool()

    result = tool.execute(
        "[1, 2, 3]"
    )

    assert result == [1, 2, 3]


def test_empty_code_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Python code cannot be empty."
    ):

        tool.execute("")


def test_none_code_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Python code cannot be empty."
    ):

        tool.execute(None)


def test_invalid_syntax_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Invalid Python syntax."
    ):

        tool.execute(
            "x ="
        )


def test_import_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Python operation is not allowed: Import"
    ):

        tool.execute(
            "import os"
        )


def test_import_from_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Python operation is not allowed: ImportFrom"
    ):

        tool.execute(
            "from os import system"
        )


def test_open_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Function 'open' is not allowed."
    ):

        tool.execute(
            'open("test.txt")'
        )


def test_os_access_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Attribute access is not allowed."
    ):

        tool.execute(
            "os.system('dir')"
        )


def test_subprocess_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Function 'subprocess' is not allowed."
    ):

        tool.execute(
            "subprocess('dir')"
        )


def test_dunder_import_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Function '__import__' is not allowed."
    ):

        tool.execute(
            "__import__('os')"
        )


def test_lambda_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Python operation is not allowed: Lambda"
    ):

        tool.execute(
            "(lambda: 10)()"
        )


def test_class_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Python operation is not allowed: ClassDef"
    ):

        tool.execute(
            """
class Test:
    pass
"""
        )


def test_function_definition_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Python statement is not allowed: FunctionDef"
    ):

        tool.execute(
            """
def test():
    return 10
"""
        )


def test_file_access_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Function 'open' is not allowed."
    ):

        tool.execute(
            'open("important.txt", "w")'
        )


def test_loop_limit_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="range\\(\\) exceeds the loop iteration limit."
    ):

        tool.execute(
            "for i in range(1001):\n    print(i)"
        )


def test_code_length_limit():

    tool = PythonExecutorTool()

    code = "x = 1\n" * 1000

    with pytest.raises(
        ValueError,
        match="Python code is too long."
    ):

        tool.execute(code)


def test_unknown_variable_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Unknown variable: secret"
    ):

        tool.execute(
            "secret + 10"
        )


def test_unknown_function_rejected():

    tool = PythonExecutorTool()

    with pytest.raises(
        ValueError,
        match="Function 'eval' is not allowed."
    ):

        tool.execute(
            "eval('10 + 20')"
        )