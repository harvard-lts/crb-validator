from crb_validator.checksum_extractor import ChecksumExtractor
from crb_validator.checksum_verifier import ChecksumVerifier
from reconciler import Reconciler
from runner import Runner
import argparse

def verify_download(args):
    runner = Runner()
    runner.run(args.download_dir, args.hydrated_dir, args.verified_dir, args.report_dir)

def reconcile_reports(args):
    reconciler = Reconciler()
    reconciler.reconcile_reports(args.report, args.inventory, args.output_dir)

def extract_checksums(args):
    checksum_extractor = ChecksumExtractor(args.batch_checksum_dir, args.report_dir)
    checksum_extractor.extract()

def final_verification(args):
    checksum_verifier = ChecksumVerifier(args.batch_dir,
                                         args.batch_checksum_dir,
                                         args.inventory,
                                         args.report_dir)
    checksum_verifier.verify(args.expedite)

###
## Main ##
###
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=
                    'Verify OCFL objects that have already been downloaded '\
                    'and rehydrated. '\
                    'Can be invoked to either move verified objects to '\
                    'provided directory and create a CSV report in the '\
                    'provided directory; or '
                    'to reconcile the CSV report created in the other '\
                    'invocation with a complete inventory CSV (created with '\
                    'the crb-inventory tool: \n'\
                    '- https://github.huit.harvard.edu/anw822/crb-inventory')

    # Create subparsers for the two modes of operation
    subparsers = ap.add_subparsers(dest='mode', help='Mode of operation')
    subparsers.required = True

    # Create the parser for the "verify" command
    verify_parser = subparsers.add_parser('verify', help='Verify objects')

    verify_parser.add_argument('-d', '--download_dir',
                  required=True,
                  help='Path to the directory containing downloaded objects')
    verify_parser.add_argument('-y', '--hydrated_dir',
                  required=True,
                  help='Path to the directory containing hydrated objects')
    verify_parser.add_argument('-v', '--verified_dir',
                  required=True,
                  help='Path to the target directory for verified objects')
    verify_parser.add_argument('-o', '--report_dir',
                  required=True,
                  help='Path to the directory to which the report will be written')
    verify_parser.set_defaults(func=verify_download)

    # Create the parser for the "reconcile" command
    reconcile_parser = subparsers.add_parser('reconcile', help='Reconcile reports.')
    reconcile_parser.add_argument('-r', '--report',
                  required=True,
                  help='Path to the report CSV file')
    reconcile_parser.add_argument('-i', '--inventory',
                  required=True,
                  help='Path to the inventory CSV file')
    reconcile_parser.add_argument('-o', '--output_dir',
                  required=True,
                  help='Path to the directory to which the reconciled report will be written')
    reconcile_parser.set_defaults(func=reconcile_reports)

    # Create the parser for the "checksums" command
    checksums_parser = subparsers.add_parser('checksums', help='Generate checksum files.',
                  description='Generate checksum files for the objects in the provided directory.')
    checksums_parser.add_argument('-c', '--batch_checksum_dir',
                  required=True,
                  help='Path to the directory of object directories to which checksums will be written')
    checksums_parser.add_argument('-r', '--report_dir',
                  required=True,
                  help='Path to the directory to which the report will be written')
    checksums_parser.set_defaults(func=extract_checksums)

    # Create the parser for the "final" verification command
    final_parser = subparsers.add_parser('final', help='Final comparison of files and checksums.')
    final_parser.add_argument('-b', '--batch_dir',
                  required=True,
                  help='Path to the directory of object directories that contains image files to be verfied')
    final_parser.add_argument('-c', '--batch_checksum_dir',
                  required=True,
                  help='Path to the directory of object directories to which checksums will be written')
    final_parser.add_argument('-i', '--inventory',
                  required=True,
                  help='Path to the inventory CSV file')
    final_parser.add_argument('-r', '--report_dir',
                  required=True,
                  help='Path to the directory to which the report will be written')
    final_parser.add_argument('-x', '--expedite',
                  required=False,
                  default=False,
                  action='store_true',
                  help='Only perform file count comparision. Skip checksum calculations.')
    final_parser.set_defaults(func=final_verification)

    args = ap.parse_args()
    args.func(args)
