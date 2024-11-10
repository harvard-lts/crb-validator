import os
class RateUtils:

    def __init__(self):
        pass

    
    def _get_objects_per_min(self, num_objects, time_seconds):
        """
        Calculate the processing rate in objects per second
        """
        # Calculate the num_objects per second
        objs_per_sec = num_objects / time_seconds

        # Convert to objects per minute
        objs_per_min = objs_per_sec * 60

        return int(objs_per_min)
    

    def _get_objects_per_min_formatted(self, num_objects, time_seconds):
        """
        Calculate the processing rate in objects per minute
        """
        objs_per_min = self._get_objects_per_min(num_objects, time_seconds)

        # Format the output with no decimal points
        formatted_speed = f"{int(objs_per_min)} / min"
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
        elapsed_time = int(end_time - start_time) | 1
        total_objects = len(os.listdir(target_dir))
        hours, minutes, seconds = self._get_timing_summary(start_time,
                                                          end_time)
        formatted_rate = self._get_objects_per_min_formatted(total_objects,
                                                             elapsed_time)

        summary = "\n======================\n"\
        "Summary:\n"\
        f"  Processing time: {hours}h:{minutes}m:{seconds}s\n"\
        f"  Total objects: {total_objects}\n"\
        f"  Processing rate: {formatted_rate}\n"\
        "======================"

        return summary