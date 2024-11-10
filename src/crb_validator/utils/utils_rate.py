import os


class RateUtils:

    def __init__(self):
        pass
  

    def _get_dir_size(self, dir):
        """
        Get the size of a directory in bytes
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                # Only add file size if it's a file
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)

        return total_size

        
    def _convert_size(self, size_bytes):
        """
        Convert size in bytes to megabytes for better readability
        """
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(min(len(size_name) - 1, (size_bytes).bit_length() // 10))
        p = 1024 ** i
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
    
    
    
    def _get_bytes_per_min(self, size_bytes, time_seconds):
        """
        Calculate the download rate in bytes per second
        """
        # Calculate the bytes per second
        bytes_per_sec = size_bytes / time_seconds

        # Convert to bytes per minute
        bytes_per_min = bytes_per_sec * 60

        return int(bytes_per_min)
    

    def _get_bytes_per_min_formatted(self, size_bytes, time_seconds):
        """
        Calculate the download rate in bytes per second
        """
        bytes_per_min = self._get_bytes_per_min(size_bytes, time_seconds)

        # Define units
        units = ['bytes/min', 'KB/min', 'MB/min', 'GB/min', 'TB/min']
        index = 0

        # Convert the speed to the appropriate unit
        while bytes_per_min >= 1024 and index < len(units) - 1:
            bytes_per_min /= 1024
            index += 1

        # Format the output with no decimal points
        formatted_speed = f"{int(bytes_per_min)} {units[index]}"
        return formatted_speed

    
    def _get_timing_summary(self, start_time, end_time):
        """
        Get a summary of the timing
        """
        elapsed_time = int(end_time - start_time)
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = elapsed_time % 60
        return hours, minutes, seconds


    def get_summary(self, target_dir, start_time, end_time):
        elapsed_time = int(end_time - start_time)
        total_size = self._get_dir_size(target_dir)
        hours, minutes, seconds = self._get_timing_summary(start_time,
                                                          end_time)
        formatted_rate = self._get_bytes_per_min_formatted(total_size,
                                                           elapsed_time)

        summary = "\n======================\n"\
        "Summary:\n"\
        f"  Processing time: {hours}h:{minutes}m:{seconds}s\n"\
        f"  Total size: {self._convert_size(total_size)}\n"\
        f"  Processing rate: {formatted_rate}\n"\
        "======================"

        return summary