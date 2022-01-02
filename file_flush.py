import io

__all__ = ["FileFlush"]


class FileFlush(io.FileIO):
    """
    Overrides FileIO to flush buffer after data writing
    """

    def __init__(self, file):
        self.file = file

    def write(self, data):
        self.file.write(data)
        self.file.flush()
