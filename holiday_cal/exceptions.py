""" Custom Exceptions """


class BaseException(Exception):
    """Base class for other exceptions"""
    pass

class ValueTooLarge(BaseException):
    """Raised when the user enters country-code that is longer than 2 """
    pass

class NoStateRegion(BaseException):
    """ Raised when the user state/region is not supported by API """
    pass