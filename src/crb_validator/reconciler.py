

import csv
from crb_validator import configure_logger
from crb_validator.csv_report import CSVReport


class Reconciler():
    def __init__(self):
        self.logger = configure_logger(__name__)

    def reconcile_reports(self, report_csv, inventory_csv, output_dir):
        self.logger.info(f"Reconciling report: {report_csv} "\
                         f"with inventory: {inventory_csv}")

        # Read the report and inventory CSVs
        input_report = self._load_csv(report_csv)
        input_inventory = self._load_csv(inventory_csv)

        # For each object in the report, check if it is in the inventory
        results = self._reconcile(report_csv, input_report, input_inventory)

        # Write the reconciled report to the same directory as the input inventory,
        #  in the format: reconciled_inventory_<timestamp>.csv
        self._write_csv(results, output_dir)
        self.logger.info("Reconciliation complete: {}")

    def _reconcile(self, report_csv, input_report, input_inventory):
        for entry in input_report:
            if entry['OSN'] in [obj['OSN'] for obj in input_inventory]:
                # If it is, compare the file-counts
                inventory_entry = next(obj for obj in input_inventory if obj['OSN'] == entry['OSN'])

                # Identify the source report in the inventory
                inventory_entry['REPORT'] = report_csv
                if entry['FILE_COUNT'] == inventory_entry['FILE_COUNT']:
                    # If they match, set the object's verified value as 'true'
                    inventory_entry['VERIFIED'] = 'true'
                else:
                    # If they don't match, set the object's verified value as the reported file-count
                    self.logger.error(f"Object {entry['OSN']} has a mismatched file-count")
                    inventory_entry['VERIFIED'] = entry['FILE_COUNT']
            else:
                # If the object is not in the inventory, add the object to the inventory with the verified values as the reported file-count
                self.logger.error(f"Object {entry['OSN']} not found in inventory")
                new_entry = {}
                new_entry['OSN'] = entry['OSN']
                new_entry['REPORT'] = report_csv
                new_entry['VERIFIED'] = entry['FILE_COUNT']
                input_inventory.append(new_entry)

        return input_inventory

    def _write_csv(self, data, output_dir):
        # Write the reconciled inventory to a new CSV file
        output_csv = CSVReport(output_dir, base_name="reconciled_inventory")
        output_csv.set_entries(data)
        output_csv.generate_csv(self._fieldnames())

    def _fieldnames(self):
        return ['PDS_LIST_URN',
                'URN',
                'OBJ_ID',
                'OSN',
                'FILE_COUNT',
                'FILE_BYTES',
                'VERIFIED',
                'REPORT']

    def _load_csv(self, csv_file):
        self.logger.debug(f"Loading report: {csv_file}")
        # Read the report CSV and return a list of entries
        entries = []
        with open (csv_file, 'r') as f:
            csvreader = csv.DictReader(f)
            for row in csvreader:
                entries.append(row)

        return entries
