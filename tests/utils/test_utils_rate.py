import pytest
from crb_validator.utils.utils_rate import RateUtils

@pytest.fixture
def rate_utils():
    return RateUtils()

def test_get_objects_per_min(rate_utils):
    # Test the get_objects_per_min method
    rate = rate_utils._get_objects_per_min(1024, 1)
    assert rate == 61440.0
    rate = rate_utils._get_objects_per_min(1048576, 1)
    assert rate == 62914560.0
    rate = rate_utils._get_objects_per_min(1073741824, 1)
    assert rate == 64424509440.0


def test_get_objects_per_min_formatted(rate_utils):
    # Test the get_objects_per_min_formatted method
    rate = rate_utils._get_objects_per_min_formatted(1024, 1)
    assert rate == "61440 / min"
    rate = rate_utils._get_objects_per_min_formatted(1048576, 1)
    assert rate == "62914560 / min"
    rate = rate_utils._get_objects_per_min_formatted(1073741824, 1)
    assert rate == "64424509440 / min"


def test_get_timing_summary(rate_utils):
    start_time = 1728761333.8907504
    end_time = 1728761527.1704545

    # Test the get_timing_summary method
    hours, minutes, seconds = rate_utils._get_timing_summary(start_time, end_time)
    assert hours == 0
    assert minutes == 3
    assert seconds == 13


def test_summary(rate_utils):
    start_time = 1728761333.8907504
    end_time = 1728761527.1704545

    # Test the get_summary method
    summary = rate_utils.get_summary("tests", start_time, end_time)
    print(f"{summary}")
