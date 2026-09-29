import pytest

from tools.calculator import CalculatorTool


@pytest.fixture
def calculator():

    return CalculatorTool()


def test_calculator_name(calculator):

    assert calculator.name == "calculator"


def test_calculator_description(calculator):

    assert calculator.description


def test_addition(calculator):

    assert calculator.execute("2 + 3") == 5


def test_subtraction(calculator):

    assert calculator.execute("10 - 4") == 6


def test_multiplication(calculator):

    assert calculator.execute("5 * 6") == 30


def test_division(calculator):

    assert calculator.execute("20 / 4") == 5


def test_floor_division(calculator):

    assert calculator.execute("20 // 3") == 6


def test_modulo(calculator):

    assert calculator.execute("10 % 3") == 1


def test_power(calculator):

    assert calculator.execute("2 ** 8") == 256


def test_negative_number(calculator):

    assert calculator.execute("-10") == -10


def test_positive_unary_operator(calculator):

    assert calculator.execute("+10") == 10


def test_parentheses(calculator):

    assert calculator.execute(
        "(2 + 3) * 4"
    ) == 20


def test_operator_precedence(calculator):

    assert calculator.execute(
        "2 + 3 * 4"
    ) == 14


def test_decimal_calculation(calculator):

    assert calculator.execute(
        "2.5 * 4"
    ) == 10.0


def test_nested_expression(calculator):

    assert calculator.execute(
        "((10 + 5) * 2) - 4"
    ) == 26


def test_empty_expression(calculator):

    with pytest.raises(ValueError):

        calculator.execute("")


def test_none_expression(calculator):

    with pytest.raises(ValueError):

        calculator.execute(None)


def test_invalid_expression(calculator):

    with pytest.raises(ValueError):

        calculator.execute("2 +")


def test_boolean_rejected(calculator):

    with pytest.raises(ValueError):

        calculator.execute("True")


def test_string_rejected(calculator):

    with pytest.raises(ValueError):

        calculator.execute('"hello"')


def test_function_call_rejected(calculator):

    with pytest.raises(ValueError):

        calculator.execute("abs(-5)")


def test_import_style_expression_rejected(calculator):

    with pytest.raises(ValueError):

        calculator.execute(
            "__import__('os')"
        )


def test_file_access_rejected(calculator):

    with pytest.raises(ValueError):

        calculator.execute(
            "open('test.txt')"
        )


def test_attribute_access_rejected(calculator):

    with pytest.raises(ValueError):

        calculator.execute(
            "().__class__"
        )


def test_zero_division_rejected(calculator):

    with pytest.raises(ValueError):

        calculator.execute("10 / 0")


def test_unsupported_operator_rejected(calculator):

    with pytest.raises(ValueError):

        calculator.execute("2 << 3")