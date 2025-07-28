import pytest
from pydantic import ValidationError

from shared.formatters import BoolConverter


def test_truthy_values():
    # Testes com valores considerados verdadeiros
    truthy_cases = ["y", "yes", "true", "1", "Y", "YES", "True", 1, True]
    for value in truthy_cases:
        converter = BoolConverter(value=value)
        assert converter.as_bool() is True


def test_falsy_values():
    # Testes com valores considerados falsos
    falsy_cases = ["n", "no", "false", "0", "N", "NO", "False", 0, False]
    for value in falsy_cases:
        converter = BoolConverter(value=value)
        assert converter.as_bool() is False


def test_invalid_values():
    # Testes com valores inválidos
    invalid_cases = ["maybe", "yes!", "  ", "123", None, {}, [], "tru", "fal"]
    for value in invalid_cases:
        with pytest.raises(ValueError):
            converter = BoolConverter(value=value)
            converter.as_bool()


def test_strip_and_case_insensitivity():
    # Testes com espaços em branco e diferentes combinações de maiúsculas e minúsculas
    test_cases = {
        "   y   ": True,
        " Yes ": True,
        "TRUE": True,
        " 0 ": False,
        "n ": False,
        "No": False,
    }
    for value, expected in test_cases.items():
        converter = BoolConverter(value=value)
        assert converter.as_bool() == expected


def test_non_string_inputs():
    # Testes com entradas que não são strings
    test_cases = {
        1: True,
        0: False,
    }
    for value, expected in test_cases.items():
        converter = BoolConverter(value=value)
        assert converter.as_bool() == expected


def test_validation_error_on_invalid_type():
    # Teste para valores que causam erro de validação no Pydantic
    invalid_cases = [123.45, object(), set(), None]
    for value in invalid_cases:
        with pytest.raises(ValidationError):
            BoolConverter(value=value)
