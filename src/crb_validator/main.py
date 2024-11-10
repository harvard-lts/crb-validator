from runner import Runner
import argparse

###
## Main ##
###
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=
                    'Verify OCFL objects that have already been downloaded '\
                    'and rehydrated.'\
                    'Moves verified objects to provided directory and '\
                    'creates a CSV report in the provided directory.')
    ap.add_argument('-d', '--download_dir',
                    required=True,
                    help='Path to the directory containing downloaded objects')
    ap.add_argument('-y', '--hydrated_dir',
                    required=True,
                    help='Path to the directory containing hydrated objects')
    ap.add_argument('-v', '--verified_dir',
                    required=True,
                    help='Path to the target directory for verified objects')
    ap.add_argument('-o', '--report_dir',
                    required=True,
                    help='Path to the directory to which the report will be written')
    args = vars(ap.parse_args())

    download_dir = args['download_dir']
    hydrated_dir = args['hydrated_dir']
    verified_dir = args['verified_dir']
    report_dir = args['report_dir']

    runner = Runner()
    runner.run(download_dir, hydrated_dir, verified_dir, report_dir)

 