import pytest
from crb_validator.validation_entry import ValidationEntry

def test_initialization():
    entry = ValidationEntry("OSN123")
    assert entry.osn == "OSN123"
    assert entry.file_count == 0
    assert entry.status == "PENDING"
    assert entry.message is None

def test_column_header():
    assert ValidationEntry.column_header() == ['OSN', 'FILE_COUNT', 'STATUS', 'MESSAGE']

def test_set_status_success():
    entry = ValidationEntry("OSN123")
    entry.set_status("SUCCESS", "All files processed")
    assert entry.status == "SUCCESS"
    assert entry.message == "All files processed"

def test_set_status_failure():
    entry = ValidationEntry("OSN123")
    entry.set_status("FAILURE", "Error processing files")
    assert entry.status == "FAILURE"
    assert entry.message == "Error processing files"

def test_set_status_invalid():
    entry = ValidationEntry("OSN123")
    with pytest.raises(ValueError, match="Invalid status: INVALID"):
        entry.set_status("INVALID")

def test_set_status_none():
    entry = ValidationEntry("OSN123")
    with pytest.raises(ValueError, match="Status cannot be None"):
        entry.set_status(None)

def test_str():
    entry = ValidationEntry("OSN123")
    assert str(entry) == "OSN123,0,PENDING"
