# exceptions

# ############################################################
# Cork
# ############################################################

class InvalidPathException(Exception):
    def __init__(self, filepath):
        Exception.__init__(self)
        self._filepath = filepath
    def __str__(self):
        return "Invalid path: \"{0}\".".format(self._filepath)


class NonExecutableException(Exception):
    def __init__(self, filepath):
        Exception.__init__(self)
        self._filepath = filepath
    def __str__(self):
        return "File not executable: \"{0}\".".format(self._filepath)


class NumberSelectionException(Exception):
    def __init__(self):
        Exception.__init__(self)
    def __str__(self):
      return "Only two objects can be selected at a time (the base object and the slice plane)"


class NonMeshSelectedException(Exception):
    def __init__(self, obj):
        Exception.__init__(self)
        self._object = obj
    def __str__(self):
      return "Selected object \"{0}\" is not a mesh".format(self._object.name)


class ExportMeshException(Exception):
    def __init__(self, obj, filepath):
        Exception.__init__(self)
        self._object = obj
        self._filepath = filepath
    def __str__(self):
      return "Failed to export object \"{0}\" to \"{1}\"".format(self._object.name, self._filepath)


class ImportMeshException(Exception):
    def __init__(self, filepath):
        Exception.__init__(self)
        self._filepath = filepath
    def __str__(self):
      return "Failed to import mesh \"{0}\"".format(self._filepath)


class ImportOffsetException(Exception):
    def __init__(self):
        Exception.__init__(self)
    def __str__(self):
        return "OFF importer not found. Enable the addon in Blender User Preferences"


# ############################################################
# Skull Import
# ############################################################

class ImportSTLException(Exception):
    def __init__(self):
        Exception.__init__(self)
    def __str__(self):
        return "STL importer not found. Enable the addon in Blender User Preferences"


class ImportSkullException(Exception):
    def __init__(self):
        Exception.__init__(self)
    def __str__(self):
        return "Failed to import skull"


class ImportSkullDecimateException(Exception):
    def __init__(self):
        Exception.__init__(self)
    def __str__(self, object_name):
        return "Failed to simplify object \"{0}\", apply the \"Decimate\" modifier manually".format(object_name)


class ImportSkullViewAllException(Exception):
    def __init__(self):
        Exception.__init__(self)
    def __str__(self):
        return "Failed to zoom out to newly import object"


