"""Tests for slugify function."""
import pytest
from packages.utils.strings import slugify


def test_slugify_simple():
    """Basic text becomes lowercase slug."""
    assert slugify("Hello World") == "hello-world"


def test_slugify_lowercase():
    """Already converts to lowercase."""
    assert slugify("UPPERCASE") == "uppercase"


def test_slugify_accents():
    """Accents are removed."""
    assert slugify("café") == "cafe"
    assert slugify("naïve") == "naive"
    assert slugify("São Paulo") == "sao-paulo"


def test_slugify_special_chars():
    """Special characters are removed."""
    assert slugify("Hello@World!") == "helloworld"
    assert slugify("price: $99") == "price-99"


def test_slugify_multi_spaces():
    """Multiple spaces become single dash."""
    assert slugify("hello   world") == "hello-world"


def test_slugify_underscores():
    """Underscores become dashes."""
    assert slugify("snake_case_text") == "snake-case-text"


def test_slugify_collapse_dashes():
    """Consecutive dashes collapse to one."""
    assert slugify("hello--world") == "hello-world"
    assert slugify("hello---world") == "hello-world"


def test_slugify_strip_dashes():
    """Leading/trailing dashes are stripped."""
    assert slugify("-hello-world-") == "hello-world"
    assert slugify("---hello---") == "hello"


def test_slugify_empty_string():
    """Empty string returns empty string."""
    assert slugify("") == ""


def test_slugify_only_special_chars():
    """Only special chars returns empty."""
    assert slugify("@#$%") == ""


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("Café au Lait", "cafe-au-lait"),
        ("Zürich", "zurich"),
        ("Łódź", "lodz"),
        ("naïveté", "naivete"),
    ],
)
def test_slugify_parametrized_accents(input_text, expected):
    """Parameterized test for various accented characters."""
    assert slugify(input_text) == expected
