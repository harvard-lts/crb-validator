import csv
from datetime import datetime
import os

from crb_validator import configure_logger
from crb_validator.validation_entry import ValidationEntry


class ValidationReport:
    def __init__(self, report_dir):
        self.logger = configure_logger(__name__)
        self.file_path = self._create_report_filepath(report_dir)
        self.entries = []


    def add_entry(self, entry):
        self.entries.append(entry)

    def generate_csv(self):
        with open(self.file_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=ValidationEntry.column_header())
            writer.writeheader()
            for entry in self.entries:
                f.write(f"{entry}\n")

    def _create_report_filepath(self, report_dir):
        # Create directory hierarchy if it doesn't exist
        os.makedirs(report_dir, exist_ok=True)

        # Create filename of form: validation_report_YYYY-MM-DD.csv
        current_date = datetime.now().strftime("%Y-%m-%d")
        csv_name = "validation_report_{}.csv".format(current_date)
        output_csv = os.path.join(report_dir, csv_name)

        index = 1
        while os.path.exists(output_csv):
            csv_name = 'validation_report_{}_{}.csv'.format(current_date, index)
            output_csv = os.path.join(report_dir, csv_name)
            index += 1

        return output_csv
