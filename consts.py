import sys

class consts:
    class ConstError(TypeError) : pass
    def __setattr__(self, key, value):
        if self.__dict__.has_key(key):
            raise self.ConstError, "Cannot rebind %s" % key
        self.__dict__[key] = value

sys.modules[__name__]=consts()

