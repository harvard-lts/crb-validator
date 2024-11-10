import os
import pytest
from project_paths import paths
from crb_validator.utils.utils_rate import RateUtils

@pytest.fixture
def size_utils():
    return RateUtils()

def test_get_dir_size(size_utils, tmp_path):
    # Create a temporary directory with some files
    d = tmp_path / "sub"
    d.mkdir()
    file1 = d / "file1.txt"
    file1.write_text("a" * 1024)  # 1 KB
    file2 = d / "file2.txt"
    file2.write_text("b" * 2048)  # 2 KB

    # Test the get_dir_size method
    size = size_utils._get_dir_size(d)
    assert size == 3072

    size_converted = size_utils._convert_size(size)
    assert size_converted == "3.0 KB"

def test_get_dir_size_empty(size_utils, tmp_path):
    # Create an empty temporary directory
    d = tmp_path / "empty"
    d.mkdir()

    # Test the get_dir_size method
    size = size_utils._get_dir_size(d)
    assert size == 0

    size_converted = size_utils._convert_size(size)
    assert size_converted == "0B"

def test_convert_size(size_utils):
    # Test the _convert_size method directly
    assert size_utils._convert_size(0) == "0B"
    assert size_utils._convert_size(1020) == "1.0 KB"
    assert size_utils._convert_size(1024) == "1.0 KB"
    assert size_utils._convert_size(1048576) == "1.0 MB"
    assert size_utils._convert_size(1073741824) == "1.0 GB"


def test_get_bytes_per_min(size_utils):
    # Test the get_bytes_per_min method
    rate = size_utils._get_bytes_per_min(1024, 1)
    assert rate == 61440.0
    rate = size_utils._get_bytes_per_min(1048576, 1)
    assert rate == 62914560.0
    rate = size_utils._get_bytes_per_min(1073741824, 1)
    assert rate == 64424509440.0


def test_get_bytes_per_min_formatted(size_utils):
    # Test the get_bytes_per_min_formatted method
    rate = size_utils._get_bytes_per_min_formatted(1024, 1)
    assert rate == "60 KB/min"
    rate = size_utils._get_bytes_per_min_formatted(1048576, 1)
    assert rate == "60 MB/min"
    rate = size_utils._get_bytes_per_min_formatted(1073741824, 1)
    assert rate == "60 GB/min"


def test_get_timing_summary(size_utils):
    start_time = 1728761333.8907504
    end_time = 1728761527.1704545

    # Test the get_timing_summary method
    hours, minutes, seconds = size_utils._get_timing_summary(start_time, end_time)
    assert hours == 0
    assert minutes == 3
    assert seconds == 13


def test_summary(size_utils):
    start_time = 1728761333.8907504
    end_time = 1728761527.1704545

    # Test the get_summary method
    summary = size_utils.get_summary("tests", start_time, end_time)
    print(f"{summary}")
