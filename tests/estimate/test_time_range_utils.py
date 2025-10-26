from decimal import InvalidOperation

import pytest

from enct.encoder import TimeRange
from enct.estimate import get_sub_time_range


def test_enc_duration_shorter():
    result = get_sub_time_range(start="100", end="200", enc_duration="50")
    assert result == TimeRange(start="100", end="150")


def test_enc_duration_longer():
    result = get_sub_time_range(start="100", end="200", enc_duration="150")
    assert result == TimeRange(start="100", end="200")


def test_enc_duration_equal():
    result = get_sub_time_range(start="100", end="200", enc_duration="100")
    assert result == TimeRange(start="100", end="200")


def test_enc_duration_zero():
    result = get_sub_time_range(start="100", end="200", enc_duration="0")
    assert result == TimeRange(start="100", end="100")


def test_decimal_inputs_shorter():
    result = get_sub_time_range(start="10.5", end="20.5", enc_duration="5.2")
    assert result == TimeRange(start="10.5", end="15.7")


def test_invalid_string_input():
    with pytest.raises(InvalidOperation):
        get_sub_time_range(start="abc", end="200", enc_duration="50")
