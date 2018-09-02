import pytest

from ..finders import shared


@pytest.mark.parametrize('expected_in, expected_out', [
    ['Mount Stuart', '"stuart"'],
    ['Argonaut Peak', '"argonaut"'],
    ['White Chuck', '"white chuck"'],
])
def test_clean_peak_name(expected_in, expected_out):
    assert shared.clean_peak_name(expected_in) == expected_out
