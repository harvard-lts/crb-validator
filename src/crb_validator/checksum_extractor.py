import os
from crb_validator import configure_logger
from crb_validator.checksum_extractor_results import ChecksumExtractorResults
from ocfl_rehydration.drs_descriptor import DrsDescriptor

from crb_validator.csv_report import CSVReport


class ChecksumExtractor:
    def __init__(self, batch_checksum_dir, report_dir):
        self.logger = configure_logger(__name__)
        self.batch_checksum_dir = batch_checksum_dir
        self.report_dir = report_dir

    def extract(self):
        """
        Extracts checksums from METS files in the batch directory
        The 'batch_checksum_dir' is the root directory containing the batch of objects,
        that initially contains directories named after the objects, each containing a METS file.
        """
        self.logger.info(f"Searching for descriptors from base: {self.batch_checksum_dir}")

        results = []

        for root, dirs, files in os.walk(self.batch_checksum_dir):
            for obj in dirs:
                result = ChecksumExtractorResults(obj)

                # Find single file with name '*mets.xml'
                obj_dir = os.path.join(root, obj)
                mets_files = [f for f in os.listdir(obj_dir) if f.endswith('mets.xml')]
                if len(mets_files) == 1:                    
                    mets_file = os.path.join(root, obj, mets_files[0])
                    self.logger.debug(f"Found METS: {mets_file}")
                    result = self._extract_checksums(mets_file, obj_dir, result)
                else:
                    result.status = "ERROR"
                    result.message = f"Expected 1 METS file in {obj_dir} but found {len(mets_files)}"
                    self.logger.error(f"Expected 1 METS file in {obj_dir} but found {len(mets_files)}")

                results.append(result)

        self._write_results(results)
    
    def _extract_checksums(self, mets_file, obj_dir, result):
        count = 0
    
        # Read in the descriptor
        descriptor = DrsDescriptor(mets_file)
        for f in descriptor.get_files().values():
            # Only process '.jp2' and '.tif' files
            image_filename = f.get_file_name()
            if image_filename.endswith('.jp2') or image_filename.endswith('.tif'):
                # Write the checksum to f.get_file_name().md5
                checksum_file = os.path.join(obj_dir, image_filename + ".md5")
                with open(checksum_file, 'w') as cf:
                    cf.write(f.get_digest_value())

                count += 1
            else:
                self.logger.debug(f"Skipping non-image file: {image_filename}")
        
        result.status = "SUCCESS"
        result.file_count = count
        return result

    def _write_results(self, results):
        # Write the results to a CSV file
        csv_report = CSVReport(self.report_dir, "checksum_extractor")
        csv_report.set_entries([r.to_dict() for r in results])
        csv_report.generate_csv(ChecksumExtractorResults.column_header())
