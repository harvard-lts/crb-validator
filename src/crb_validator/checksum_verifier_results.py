class ChecksumVerifierResults:
    def __init__(self, osn):
        self.osn = osn
        self.status = "UNKNOWN"
        self.message = ""
        self.missing = 0
        self.failed = 0
        self.success = 0

    def is_success(self):
        return self.status == "SUCCESS"
    
    @property
    def message(self):
        return f"missing:{self.missing}, failed:{self.failed}, success:{self.success}"

    @message.setter
    def message(self, value):
        self._message = value

    @staticmethod
    def column_header():
        return ['PDS_LIST_URN',
                'URN',
                'OBJ_ID',
                'OSN',
                'FILE_COUNT',
                'FILE_BYTES',
                'VERIFIED',
                'REPORT',
                'FINAL_STATUS',
                'MESSAGE']
    
    def __str__(self):
        return f"{self.osn},{self.file_count},{self.status},{self.message},{self.missing},{self.failed},{self.success}"
