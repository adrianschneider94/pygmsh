class Field(object):

    """
    Base class for the creation of size fields.
    """

    _ID = 0

    def __init__(self, type=""):
        self.id = Field._ID
        Field._ID += 1

        self._code = ["Field[{}] = {};".format(self.id, self.field_type)]
        self.field_type = type

    @property
    def code(self):
        return "\n".join(self._code)
