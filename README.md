# Chinese Rare Books Validator

This utility validates DRS objects that have been downloaded, rehydrated, and restructured.
It is the follow-on corollary to the [chinese-rare-books-downloader](https://github.com/harvard-lts/chinese-rare-books-downloader) tool.

The rehydration and restructuring is designed to use the structure and naming conventions required by the [drs-bulk-uploader](https://github.huit.harvard.edu/LTS/drs-bulk-uploader) tool.

The crb-validator validates that:
- all downloaded DRS objects are also represented in their rehydrated form
- for each object, the number of constituent files are the same in both downloaded and rehydrated forms
- for each object, the names of the rehydrated files are the original file names
- for each object, the MD5 checksums match between downloaded and rehydrated files

## Usage

To run the utility:
```bash
usage: main.py [-h] -d DOWNLOAD_DIR -y HYDRATED_DIR -v VERIFIED_DIR -o
               REPORT_DIR

Verify OCFL objects that have already been downloaded and rehydrated. Moves
verified objects to provided directory and creates a CSV report in the
provided directory.

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

## Development

```
python3.11 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python pytest
```

There are also Docker scripts for local development and publishing to the HUIT Docker registry.
