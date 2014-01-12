import sys

class globs:
    def __setattr__(self, key, value):
        self.__dict__[key] = value

sys.modules[__name__] = globs()
