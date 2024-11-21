import csv
from datetime import datetime
import os

from crb_validator import configure_logger


class CSVReport:
    def __init__(self, report_dir, base_name="validation_report"):
        self.logger = configure_logger(__name__)
        self.file_path = self._create_report_filepath(report_dir, base_name)
        self.entries = []


    def add_entry(self, entry):
        self.entries.append(entry)

    def set_entries(self, entries):
        self.entries = entries

    def generate_csv(self, fieldnames):
        with open(self.file_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.entries:
                writer.writerow(entry)

    def _create_report_filepath(self, report_dir, base_name):
        # Create directory hierarchy if it doesn't exist
        os.makedirs(report_dir, exist_ok=True)

        # Create filename of form: <base_name>_YYYY-MM-DD.csv
        current_date = datetime.now().strftime("%Y-%m-%d")
        csv_name = "{}_{}.csv".format(base_name, current_date)
        output_csv = os.path.join(report_dir, csv_name)

        index = 1
        while os.path.exists(output_csv):
            csv_name = '{}_{}_{}.csv'.format(base_name, current_date, index)
            output_csv = os.path.join(report_dir, csv_name)
            index += 1

        return output_csv
