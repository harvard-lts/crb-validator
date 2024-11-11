import hashlib
from crb_validator.utils.utils_rate import RateUtils
import os
import time
from crb_validator import configure_logger
from ocfl_rehydration.drs_file import DrsFile
from ocfl_rehydration.drs_descriptor import DrsDescriptor
from ocfl_rehydration.ocfl_inventory import OcflInventory

from crb_validator.validation_entry import ValidationEntry
from crb_validator.validation_report import ValidationReport

class Runner:

    def __init__(self):
        self.rate_utils = RateUtils()
        self.logger = configure_logger(__name__)


    def run(self, download_dir, hydrated_dir, verified_dir, report_dir):
        self.logger.info(f"Starting run with download_dir: {download_dir} "\
                         f"and hydrated_dir: {hydrated_dir}")

        # Create a validation report
        report = ValidationReport(report_dir)
        try:
            start_time = time.time()
            self._do_run(download_dir,
                         hydrated_dir,
                         verified_dir,
                         report)
        except Exception as e:
            msg = f"An error occurred during validation: {e}"
            self.logger.error(msg)
            entry = ValidationEntry("n/a")
            entry.set_status("FAILURE", msg)
            report.add_entry(entry)

        finally:
            end_time = time.time()
            report.generate_csv()
            self.logger.info(f"Report CSV: {report.file_path}")
            self.logger.debug(f"Summary of directory: {verified_dir}")
            self.logger.info(self.rate_utils.get_summary(verified_dir,
                                                         start_time,
                                                         end_time))


    def _do_run(self, download_dir, hydrated_dir, verified_dir, report):
        # Create verified directory if it doesn't exist
        os.makedirs(verified_dir, exist_ok=True)

        # Verify download and hydrated object names are the same
        download_obj_dirs = self._list_subdirectory_names(download_dir)
        hydrated_obj_dirs = self._list_subdirectory_names(hydrated_dir)
        self._verify_sets(download_obj_dirs, hydrated_obj_dirs)

        # At this point, we know the download and hydrated dirs have the same objects
        for obj in hydrated_obj_dirs:
            self.logger.info(f"Verifying object: {obj}")
            result = self._verify_objs(download_dir, hydrated_dir, obj)
            report.add_entry(result)

            # Move the hydrated object to the verified directory, if successful
            if result.status == "SUCCESS":
                hydrated_obj = os.path.join(hydrated_dir, obj)
                verified_obj = os.path.join(verified_dir, obj)
                os.rename(hydrated_obj, verified_obj)


    def _list_subdirectory_names(self, directory):
        try:
            subdirectories = [d for d in os.listdir(directory)
                              if os.path.isdir(os.path.join(directory, d))]
            return subdirectories

        except Exception as e:
            self.logger.error(f"An error occurred listing subdirectories in {directory}: {e}")
            raise e

    def _verify_sets(self, download_objs, hydrated_objs):
        # Verify download objects exist in hydrated objects
        if len(download_objs) != len(hydrated_objs):
            msg = f"Download objects: {len(download_objs)} "\
                  f"!= Hydrated objects: {len(hydrated_objs)}"
            self.logger.error(msg)
            raise FileNotFoundError(msg)
        
        # Verify download objects exist in hydrated objects
        for download_obj in download_objs:
            if download_obj not in hydrated_objs:
                msg = f"Download object {download_obj} not found "\
                      f"in hydrated objects: {hydrated_objs}"
                self.logger.error(msg)
                raise FileNotFoundError(msg)
            
    def _verify_objs(self, download_dir, hydrated_dir, obj):
        result = ValidationEntry(obj)

        # Collect hydrated objects and files
        hydrated_obj = {}

        hydrated_obj_root = os.path.join(hydrated_dir, obj)
        for file in self._list_files(hydrated_obj_root):
            hydrated_file = self._get_hydrated_file(file)
            hydrated_obj[os.path.basename(file)] = hydrated_file

        # Collect download objects and files from descriptors
        download_obj = {}

        # For each download object, read descriptor
        download_obj_root = os.path.join(download_dir, obj)
        ocfl_inventory = self._get_ocfl_inventory(download_obj_root)
        drs_descriptor = self._get_drs_descriptor(download_obj_root,
                                                  ocfl_inventory)

        for f in drs_descriptor.get_files().values():
            download_obj[f.get_file_name()] = f

        # Verify number and digests between download and hydrated objects
        try:
            self._do_verify_objs(download_obj, hydrated_obj)
            result.set_status("SUCCESS")
        except Exception as e:
            result.set_status("FAILURE", str(e))
            self.logger.error(f"Error verifying object {obj}: {e}")
            # Stop processing this object if there is an error
            return result

        result.set_file_count(len(download_obj))
        return result


    def _do_verify_objs(self, download_files, hydrated_files):
        self._verify_sets(download_files, hydrated_files)
        
        # Verify download files have the same digest as hydrated files
        for download_file in download_files:
            download_digest = download_files[download_file].get_digest_value()
            hydrated_digest = hydrated_files[download_file].get_digest_value()
            if download_digest != hydrated_digest:
                msg = f"Download file {download_file} has digest "\
                      f"{download_digest} != Hydrated digest {hydrated_digest}"
                self.logger.error(msg)
                raise ValueError(msg)
        

            
    def _list_files(self, obj_dir):
        try:
            files = [os.path.join(obj_dir, f)
                     for f in os.listdir(obj_dir) 
                     if os.path.isfile(os.path.join(obj_dir, f))]
            return files

        except Exception as e:
            self.logger.error(f"An error occurred listing files in {obj_dir}: {e}")
            raise e
            
    def _get_hydrated_file(self, file):
        """Create a file object for the given hydrated file"""
        hydrated_file = DrsFile()
        hydrated_file.set_file_name(file)
        hydrated_file.set_digest_alg("md5")
        hydrated_file.set_digest_value(self._calculate_md5(file))
        self.logger.debug(f"file: {file}, md5: {hydrated_file.get_digest_value()}")
        return hydrated_file

    def _calculate_md5(self, file_path):
        md5_hash = hashlib.md5()

        # Open the file in binary read mode
        with open(file_path, 'rb') as f:
            # Read the file in chunks to avoid memory issues with large files
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        
        # Return the hash as a hexadecimal string
        return md5_hash.hexdigest()
    

    def _get_ocfl_inventory(self, obj_root):
        inventory_path = os.path.join(obj_root, 'inventory.json')
        with open(inventory_path, 'r') as file:
            return OcflInventory(file)
        
    def _get_drs_descriptor(self, obj_root, ocfl_inventory):
        descriptor_path = ocfl_inventory.get_descriptor_path()
        return DrsDescriptor(os.path.join(obj_root, descriptor_path))

