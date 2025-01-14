import os
import tempfile
import hashlib
import csv
import pytest
from crb_validator.checksum_verifier import ChecksumVerifier
from crb_validator.checksum_verifier_results import ChecksumVerifierResults

@pytest.fixture
def setup_directories():
    with tempfile.TemporaryDirectory() as batch_dir, tempfile.TemporaryDirectory() as batch_checksum_dir, tempfile.TemporaryDirectory() as report_dir:
        yield batch_dir, batch_checksum_dir, report_dir

def create_test_files(directory, files):
    for file_name, content in files.items():
        with open(os.path.join(directory, file_name), 'w') as f:
            f.write(content)

def create_test_checksums(directory, files):
    for file_name, content in files.items():
        checksum = hashlib.md5(content.encode()).hexdigest()
        with open(os.path.join(directory, file_name + '.md5'), 'w') as f:
            f.write(checksum)

def create_inventory_csv(directory, inventory):
    inventory_csv = os.path.join(directory, 'inventory.csv')
    with open(inventory_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['file_name'])
        writer.writeheader()
        for item in inventory:
            writer.writerow({'file_name': item})
    return inventory_csv

def test_verify_file_count_success(setup_directories):
    batch_dir, batch_checksum_dir, report_dir = setup_directories
    files = {'file1.jp2': 'content1', 'file2.jp2': 'content2'}
    create_test_files(batch_dir, files)
    create_test_checksums(batch_checksum_dir, files)
    inventory_csv = create_inventory_csv(report_dir, files.keys())

    verifier = ChecksumVerifier(batch_dir, batch_checksum_dir, inventory_csv, report_dir)
    result = ChecksumVerifierResults('test_batch')
    result = verifier._verify_file_count(batch_dir, batch_checksum_dir, result)

    assert result.status == "SUCCESS"

def test_verify_file_count_failure(setup_directories):
    batch_dir, batch_checksum_dir, report_dir = setup_directories
    files = {'file1.txt': 'content1', 'file2.txt': 'content2'}
    create_test_files(batch_dir, files)
    create_test_checksums(batch_checksum_dir, {'file1.txt': 'content1'})
    inventory_csv = create_inventory_csv(report_dir, files.keys())

    verifier = ChecksumVerifier(batch_dir, batch_checksum_dir, inventory_csv, report_dir)
    result = ChecksumVerifierResults('test_batch')
    result = verifier._verify_file_count(batch_dir, batch_checksum_dir, result)

    assert result.status == "FAILED"

def test_verify_checksums_success(setup_directories):
    batch_dir, batch_checksum_dir, report_dir = setup_directories
    files = {'file1.txt': 'content1', 'file2.txt': 'content2'}
    create_test_files(batch_dir, files)
    create_test_checksums(batch_checksum_dir, files)
    inventory_csv = create_inventory_csv(report_dir, files.keys())

    verifier = ChecksumVerifier(batch_dir, batch_checksum_dir, inventory_csv, report_dir)
    result = ChecksumVerifierResults('test_batch')
    result = verifier._verify_checksums(batch_dir, batch_checksum_dir, result)

    assert result.success == 2
    assert result.failed == 0
    assert result.missing == 0

def test_verify_checksums_failure(setup_directories):
    batch_dir, batch_checksum_dir, report_dir = setup_directories
    files = {'file1.txt': 'content1', 'file2.txt': 'content2'}
    create_test_files(batch_dir, files)
    create_test_checksums(batch_checksum_dir, {'file1.txt': 'content1', 'file2.txt': 'wrong_content'})
    inventory_csv = create_inventory_csv(report_dir, files.keys())

    verifier = ChecksumVerifier(batch_dir, batch_checksum_dir, inventory_csv, report_dir)
    result = ChecksumVerifierResults('test_batch')
    result = verifier._verify_checksums(batch_dir, batch_checksum_dir, result)

    assert result.success == 1
    assert result.failed == 1
    assert result.missing == 0

def test_verify_checksums_missing(setup_directories):
    batch_dir, batch_checksum_dir, report_dir = setup_directories
    files = {'file1.txt': 'content1', 'file2.txt': 'content2'}
    create_test_files(batch_dir, files)
    create_test_checksums(batch_checksum_dir, {'file1.txt': 'content1'})
    inventory_csv = create_inventory_csv(report_dir, files.keys())

    verifier = ChecksumVerifier(batch_dir, batch_checksum_dir, inventory_csv, report_dir)
    result = ChecksumVerifierResults('test_batch')
    result = verifier._verify_checksums(batch_dir, batch_checksum_dir, result)

    assert result.success == 1
    assert result.failed == 0
    assert result.missing == 1