# Chinese Rare Books Validator

This utility has two modes of operation:

1. **Verify**: validates DRS objects that have been downloaded, rehydrated, and restructured.
It is the follow-on corollary to the [chinese-rare-books-downloader](https://github.com/harvard-lts/chinese-rare-books-downloader) tool.

The rehydration and restructuring is designed to use the structure and naming conventions required by the [drs-bulk-uploader](https://github.huit.harvard.edu/LTS/drs-bulk-uploader) tool.

The crb-validator validates that:
- all downloaded DRS objects are also represented in their rehydrated form
- for each object, the number of constituent files are the same in both downloaded and rehydrated forms
- for each object, the names of the rehydrated files are the original file names
- for each object, the MD5 checksums match between downloaded and rehydrated files

2. **Reconcile**: reconciles the report created by the **verify** function of this utility with
the corresponding entries in the inventory spreadsheet created by the [crb-inventory](https://github.huit.harvard.edu/anw822/crb-inventory) tool.

For each entry in the 'verify report', this mode of operation verifies that:
- the entry is in the inventory
- the file_count for the entry in the report and inventory are equal

## Usage

To run the utility:
### Overview
```bash
usage: main.py [-h] {verify,reconcile} ...

Verify OCFL objects that have already been downloaded and rehydrated. Can be
invoked to either move verified objects to provided directory and create a CSV
report in the provided directory; or to reconcile the CSV report created in
the other invocation with a complete inventory CSV (created with the crb-
inventory tool: - https://github.huit.harvard.edu/anw822/crb-inventory

positional arguments:
  {verify,reconcile}  Mode of operation
    verify            Verify objects
    reconcile         Reconcile reports.

options:
  -h, --help          show this help message and exit
```

### Verify
```bash
usage: main.py verify [-h] -d DOWNLOAD_DIR -y HYDRATED_DIR -v VERIFIED_DIR -o
                      REPORT_DIR

options:
  -h, --help            show this help message and exit
  -d DOWNLOAD_DIR, --download_dir DOWNLOAD_DIR
                        Path to the directory containing downloaded objects
  -y HYDRATED_DIR, --hydrated_dir HYDRATED_DIR
                        Path to the directory containing hydrated objects
  -v VERIFIED_DIR, --verified_dir VERIFIED_DIR
                        Path to the target directory for verified objects
  -o REPORT_DIR, --report_dir REPORT_DIR
                        Path to the directory to which the report will be
                        written
```

### Reconcile
```bash
usage: main.py reconcile [-h] -r REPORT -i INVENTORY -o OUTPUT_DIR

options:
  -h, --help            show this help message and exit
  -r REPORT, --report REPORT
                        Path to the report CSV file
  -i INVENTORY, --inventory INVENTORY
                        Path to the inventory CSV file
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Path to the directory to which the reconciled report
                        will be written
```

## Development

```
python3.11 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python pytest
```

There are also Docker scripts for local development and publishing to the HUIT Docker registry.
