import csv
import hashlib
import os

from crb_validator import configure_logger
from crb_validator.checksum_verifier_results import ChecksumVerifierResults
from crb_validator.csv_report import CSVReport


class ChecksumVerifier:
    def __init__(self, batch_dir, batch_checksum_dir, inventory_csv, report_dir):
        self.logger = configure_logger(__name__)
        self.batch_dir = batch_dir
        self.batch_checksum_dir = batch_checksum_dir
        self.report_dir = report_dir
        self.input_inventory = self._load_csv(inventory_csv)
        self.report = []

    def verify(self, expedited=False):
        # Get the list of directories in the batch directory
        batch_dirs = [d for d in os.listdir(self.batch_dir) if os.path.isdir(os.path.join(self.batch_dir, d))]

        results = []

        # Iterate over the directories
        for d in batch_dirs:
            result = ChecksumVerifierResults(d)

            # Content/Image file directory
            files_dir = os.path.join(self.batch_dir, d)

            # Checksums file directory
            checksums_dir = os.path.join(self.batch_checksum_dir, d)

            # Verify number of files equals number of checksums
            result = self._verify_file_count(files_dir, checksums_dir, result)

            # Verify checksums
            if result.is_success() and not expedited:
                result = self._verify_checksums(files_dir, checksums_dir, result)
    
            results.append(result)

            self.logger.info(f"Checksum verification complete for: {d}: {result.status}")

        # Add results to the inventory
        report = self._add_results_to_report(results, self.input_inventory)

        self.logger.info(f"Checksum verification complete for all {len(batch_dirs)} objects")
        self._write_results(report)


    def _verify_file_count(self, files_dir, checksums_dir, result):
        """
        Verify the number of files in the OSN directory equals the number of checksum files
        """
        self.logger.debug(f"Verifying file count in {files_dir}")

        # Get the list of files in the directory
        files = [f for f in os.listdir(files_dir) if os.path.isfile(os.path.join(files_dir, f))]

        # Verify number of files equals number of checksums
        checksum_files = [f for f in os.listdir(checksums_dir) if f.endswith('.md5')]

        if len(files) == len(checksum_files):
            result.status = "SUCCESS"
            result.message = f"Expedited checksum verification: {len(files)} files"
        else:
            result.status = "FAILED"
            result.message = f"Expected {len(files)} checksum files but found {len(checksum_files)}"

        return result
    
    def _verify_checksums(self, files_dir, checksums_dir, result):
        """
        Verify the checksums of the files in the OSN directory
        """
        self.logger.debug(f"Verifying checksums in {files_dir}")

        missing = 0
        failed = 0
        success = 0

        # Get the list of files in the directory
        files = [f for f in os.listdir(files_dir) if os.path.isfile(os.path.join(files_dir, f))]

        # Iterate over the files
        for f in files:
            # Get the file path
            file_path = os.path.join(files_dir, f)

            # Get the checksum file path
            checksum_file_path = os.path.join(checksums_dir, f + '.md5')
            
            # Check if the checksum file exists
            if os.path.exists(checksum_file_path):
                # Read the checksum from the checksum file
                with open(checksum_file_path, 'r') as checksum_file:
                    checksum = checksum_file.read().strip()

                # Calculate the checksum of the file
                file_checksum = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

                # Compare the checksums
                if checksum == file_checksum:
                    success += 1
                else:
                    self.logger.error(f"Checksum mismatch: {f}: {checksum} != {file_checksum}")
                    result.status = "FAILED"
                    failed += 1
            else:
                self.logger.error(f"Checksum file not found: {checksum_file_path}")
                result.status = "FAILED"
                missing += 1

        result.missing = missing
        result.failed = failed
        result.success = success

        return result
    
    def _add_results_to_report(self, results, input_inventory):
        """
        Add the results to the inventory
        """
        self.logger.debug("Adding results to inventory")

        # Iterate over the results
        for r in results:
            # Check if the object is in the inventory
            if r.osn in [obj['OSN'] for obj in input_inventory]:
                # If it is, compare the file-counts
                inventory_entry = next(obj for obj in input_inventory if obj['OSN'] == r.osn)

                inventory_entry['FINAL_STATUS'] = r.status
                inventory_entry['MESSAGE'] = r.message
            else:
                # If the object is not in the inventory, add the object to the inventory with the verified values as the reported file-count
                self.logger.error(f"Object {r.osn} not found in inventory")
                new_entry = {}
                new_entry['OSN'] = r.osn
                new_entry['FINAL_STATUS'] = r.status
                new_entry['MESSAGE'] = r.message
                input_inventory.append(new_entry)

        return input_inventory
    

    def _load_csv(self, csv_file):
        self.logger.debug(f"Loading report: {csv_file}")
        # Read the report CSV and return a list of entries
        entries = []
        with open (csv_file, 'r') as f:
            csvreader = csv.DictReader(f)
            for row in csvreader:
                entries.append(row)

        return entries
    
    def _write_results(self, results):
        # Write the results to a CSV file
        csv_report = CSVReport(self.report_dir, "checksum_verifier")
        csv_report.set_entries(results)
        csv_report.generate_csv(ChecksumVerifierResults.column_header())