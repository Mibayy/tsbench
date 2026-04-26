import pytest

from packages.utils.slugify import slugify


def test_simple():
    assert slugify("Hello World") == "hello-world"


def test_accents():
    assert slugify("Éléphant à Paris") == "elephant-a-paris"


def test_multi_spaces():
    assert slugify("foo   bar    baz") == "foo-bar-baz"


def test_trailing_and_leading_spaces():
    assert slugify("   hello world   ") == "hello-world"


def test_empty_string():
    assert slugify("") == ""


def test_special_characters():
    assert slugify("Rock & Roll 100%") == "rock-roll-100"


def test_collapse_consecutive_dashes():
    assert slugify("a---b--c") == "a-b-c"


def test_strip_edge_dashes():
    assert slugify("---hello---") == "hello"


def test_only_special_chars():
    assert slugify("&%&%") == ""


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Café Crème", "cafe-creme"),
        ("  Ça va ?  ", "ca-va"),
        ("naïve façade", "naive-facade"),
    ],
)
def test_parametrized_accents(raw, expected):
    assert slugify(raw) == expected
