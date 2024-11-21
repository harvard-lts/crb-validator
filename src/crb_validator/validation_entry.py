class ValidationEntry:
    def __init__(self, osn):
        self.osn = osn
        self.file_count = 0
        self.status = "PENDING"
        self.message = None

    @staticmethod
    def column_header():
        return ['OSN', 'FILE_COUNT', 'STATUS', 'MESSAGE']
    
    def set_status(self, status, message=None):
        if status is None:
            raise ValueError("Status cannot be None")

        status = status.upper()
        if status not in ["PENDING", "SUCCESS", "FAILURE"]:
            raise ValueError(f"Invalid status: {status}")

        if message is not None:
            self.message = message
        
        self.status = status


    def set_file_count(self, count):
        self.file_count = count

    def to_dict(self):
        if self.message:
            return {
                'OSN': self.osn,
                'FILE_COUNT': self.file_count,
                'STATUS': self.status,
                'MESSAGE': self.message
            }
        else:
            return {
                'OSN': self.osn,
                'FILE_COUNT': self.file_count,
                'STATUS': self.status
            }


    def __str__(self):
        if self.message:
            return f"{self.osn},{self.file_count},{self.status},{self.message}"
        else:
            return f"{self.osn},{self.file_count},{self.status}"
