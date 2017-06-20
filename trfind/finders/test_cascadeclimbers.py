import pytest

import trfind.finders.cascadeclimbers as module


@pytest.mark.parametrize('expected_in, expected_out', [
    ['Mount Stuart', '"stuart"'],
    ['Argonaut Peak', '"argonaut"'],
    ['White Chuck', '"white chuck"'],
])
def test_clean_name_for_cacadeclimbers(expected_in, expected_out):
    assert module._clean_name_for_cascadeclimbers(expected_in) == expected_out
