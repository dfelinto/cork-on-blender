# exceptions

class InvalidPathException(Exception):
    def __init__(self, filepath):
        self._filepath = filepath

    def __str__(self):
        return "Invalid path: \"{0}\".".format(self._filepath)


class NonExecutableException(Exception):
    def __init__(self, filepath):
        self._filepath = filepath

    def __str__(self):
        return "File not executable: \"{0}\".".format(self._filepath)

