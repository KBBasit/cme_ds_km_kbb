import pytest
from src.gdelt import fetch_data



def test_valid_mode():
    with pytest.raises(ValueError):
        fetch_data("Oil", mode="this_mode_does_not_exist")


def test_valid_timespan():
    with pytest.raises(ValueError):
        fetch_data("Oil", timespan="this_timespan_does_not_exist")
