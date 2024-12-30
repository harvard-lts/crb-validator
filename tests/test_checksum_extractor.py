import os
import pytest
from unittest.mock import ANY, MagicMock, patch
from crb_validator.checksum_extractor import ChecksumExtractor
from crb_validator.checksum_extractor_results import ChecksumExtractorResults

@pytest.fixture
def checksum_extractor(tmp_path):
    base_dir = tmp_path / "base"
    base_dir.mkdir()
    report_dir = tmp_path / "report"
    report_dir.mkdir()
    return ChecksumExtractor(base_dir, report_dir)

def test_extract_single_mets_file(checksum_extractor, tmp_path, caplog):
    obj_dir = tmp_path / "base" / "obj1"
    obj_dir.mkdir(parents=True)
    mets_file = obj_dir / "file1.mets.xml"
    mets_file.touch()

    with patch("os.walk", return_value=[(tmp_path / "base", ["obj1"], [])]), \
         patch("os.listdir", return_value=["file1.mets.xml"]), \
         patch.object(checksum_extractor, "_extract_checksums") as mock_extract_checksums, \
         patch.object(checksum_extractor, "_write_results") as mock_write_results:
        
        checksum_extractor.extract()
        mock_extract_checksums.assert_called_once_with(str(mets_file), str(obj_dir), ANY)
        mock_write_results.assert_called_once()

def test_extract_multiple_mets_files(checksum_extractor, tmp_path, caplog):
    obj_dir = tmp_path / "base" / "obj1"
    obj_dir.mkdir(parents=True)
    (obj_dir / "file1.mets.xml").touch()
    (obj_dir / "file2.mets.xml").touch()

    with patch("os.walk", return_value=[(tmp_path / "base", ["obj1"], [])]), \
         patch("os.listdir", return_value=["file1.mets.xml", "file2.mets.xml"]), \
         patch.object(checksum_extractor, "_write_results") as mock_write_results:
        
        checksum_extractor.extract()
        assert "Expected 1 METS file" in caplog.text
        mock_write_results.assert_called_once()

def test_extract_no_mets_files(checksum_extractor, tmp_path, caplog):
    obj_dir = tmp_path / "base" / "obj1"
    obj_dir.mkdir(parents=True)

    with patch("os.walk", return_value=[(tmp_path / "base", ["obj1"], [])]), \
         patch("os.listdir", return_value=[]), \
         patch.object(checksum_extractor, "_write_results") as mock_write_results:
        
        checksum_extractor.extract()
        assert "Expected 1 METS file" in caplog.text
        mock_write_results.assert_called_once()

def test_extract_checksums_success(checksum_extractor, tmp_path):
    obj_dir = tmp_path / "base" / "obj1"
    obj_dir.mkdir(parents=True)
    mets_file = obj_dir / "file1.mets.xml"
    mets_file.touch()

    mock_descriptor = MagicMock()
    mock_file = MagicMock()
    mock_file.get_file_name.return_value = "file1.jp2"
    mock_file.get_digest_value.return_value = "dummy_checksum"
    mock_descriptor.get_files.return_value = {"file1.jp2": mock_file}

    with patch("crb_validator.checksum_extractor.DrsDescriptor", return_value=mock_descriptor):
        result = ChecksumExtractorResults("obj1")
        result = checksum_extractor._extract_checksums(str(mets_file), str(obj_dir), result)
        
        checksum_file = obj_dir / "file1.jp2.md5"
        assert checksum_file.exists()
        with open(checksum_file, 'r') as cf:
            assert cf.read() == "dummy_checksum"
        
        assert result.status == "SUCCESS"
        assert result.file_count == 1

def test_extract_checksums_multiple_files(checksum_extractor, tmp_path):
    obj_dir = tmp_path / "base" / "obj1"
    obj_dir.mkdir(parents=True)
    mets_file = obj_dir / "file1.mets.xml"
    mets_file.touch()

    mock_descriptor = MagicMock()
    mock_file1 = MagicMock()
    mock_file1.get_file_name.return_value = "file1.tif"
    mock_file1.get_digest_value.return_value = "checksum1"
    mock_file2 = MagicMock()
    mock_file2.get_file_name.return_value = "file2.tif"
    mock_file2.get_digest_value.return_value = "checksum2"
    mock_descriptor.get_files.return_value = {"file1.tif": mock_file1, "file2.tif": mock_file2}

    with patch("crb_validator.checksum_extractor.DrsDescriptor", return_value=mock_descriptor):
        result = ChecksumExtractorResults("obj1")
        result = checksum_extractor._extract_checksums(str(mets_file), str(obj_dir), result)
        
        checksum_file1 = obj_dir / "file1.tif.md5"
        checksum_file2 = obj_dir / "file2.tif.md5"
        assert checksum_file1.exists()
        assert checksum_file2.exists()
        with open(checksum_file1, 'r') as cf1, open(checksum_file2, 'r') as cf2:
            assert cf1.read() == "checksum1"
            assert cf2.read() == "checksum2"
        
        assert result.status == "SUCCESS"
        assert result.file_count == 2

def test_extract_checksums_no_files(checksum_extractor, tmp_path):
    obj_dir = tmp_path / "base" / "obj1"
    obj_dir.mkdir(parents=True)
    mets_file = obj_dir / "file1.mets.xml"
    mets_file.touch()

    mock_descriptor = MagicMock()
    mock_descriptor.get_files.return_value = {}

    with patch("crb_validator.checksum_extractor.DrsDescriptor", return_value=mock_descriptor):
        result = ChecksumExtractorResults("obj1")
        result = checksum_extractor._extract_checksums(str(mets_file), str(obj_dir), result)
        
        assert result.status == "SUCCESS"
        assert result.file_count == 0

def test_write_results(checksum_extractor, tmp_path):
    results = [
        ChecksumExtractorResults("obj1"),
        ChecksumExtractorResults("obj2")
    ]
    results[0].status = "SUCCESS"
    results[0].file_count = 1
    results[1].status = "ERROR"
    results[1].message = "Some error"

    with patch("crb_validator.checksum_extractor.CSVReport") as MockCSVReport:
        mock_csv_report = MockCSVReport.return_value
        checksum_extractor._write_results(results)
        
        MockCSVReport.assert_called_once_with(checksum_extractor.report_dir, "checksum_extractor")
        mock_csv_report.set_entries.assert_called_once_with([r.to_dict() for r in results])
        mock_csv_report.generate_csv.assert_called_once_with(ChecksumExtractorResults.column_header())


def test_extract_checksums_skips_non_image_files(checksum_extractor, tmp_path):
    obj_dir = tmp_path / "base" / "obj1"
    obj_dir.mkdir(parents=True)
    mets_file = obj_dir / "file1.mets.xml"
    mets_file.touch()

    mock_descriptor = MagicMock()
    mock_file = MagicMock()
    mock_file.get_file_name.return_value = "file1.txt"
    mock_descriptor.get_files.return_value = {"file1.txt": mock_file}

    with patch("crb_validator.checksum_extractor.DrsDescriptor", return_value=mock_descriptor):
        result = ChecksumExtractorResults("obj1")
        result = checksum_extractor._extract_checksums(str(mets_file), str(obj_dir), result)
        
        checksum_file = obj_dir / "file1.txt.md5"
        assert not checksum_file.exists()
        
        assert result.status == "SUCCESS"
        assert result.file_count == 0


