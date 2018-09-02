import pytest

from . import shared
from .stephabegg import remove_mount


@pytest.mark.parametrize('expected_in, expected_out', [
    ['Mount Stuart', '"stuart"'],
    ['Argonaut Peak', '"argonaut"'],
    ['White Chuck', '"white chuck"'],
])
def test_clean_peak_name(expected_in, expected_out):
    assert shared.clean_peak_name(expected_in) == expected_out


@pytest.mark.parametrize('expected_in, expected_out', [
    ['mount stuart', ' stuart'],
    ['mountstuart', 'stuart'],
    ['argonaut', 'argonaut'],
    ['mt stuart', 'mt stuart'],
])
def test_remove_mount(expected_in, expected_out):
    assert remove_mount(expected_in) == expected_out
