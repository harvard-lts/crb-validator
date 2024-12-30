class ChecksumExtractorResults:
    def __init__(self, osn):
        self.osn = osn
        self.status = "UNKNOWN"
        self.message = ""
        self.file_count = 0

    @staticmethod
    def column_header():
        return ['OSN', 'FILE_COUNT', 'STATUS', 'MESSAGE']

    def to_dict(self):
        return {
            "OSN": self.osn,
            "FILE_COUNT": self.file_count,
            "STATUS": self.status,
            "MESSAGE": self.message,
            
        }
    
    def __str__(self):
        return f"{self.osn},{self.file_count},{self.status},{self.message}"