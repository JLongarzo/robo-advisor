import pytest

from app.robo_advisor import hasNumbers, to_usd


def test_to_usd():

    result = to_usd(40.5)
    assert result == "$40.50"

    result = to_usd(39.19294094)
    assert result == "$39.19"


def test_hasNumbers():
    result = hasNumbers("TSLA")
    assert result == False

    result = hasNumbers("1TQ4")
    assert result == True
