class EncoderFailureException(Exception):
    def __init__(self, message: str, stderr: str):
        self.stderr = stderr
        super().__init__(message)


class EmptyEncodedException(Exception):
    def __init__(self, message: str, stderr: str):
        self.stderr = stderr
        super().__init__(message)
