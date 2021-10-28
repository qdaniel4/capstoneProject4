""" Custom Exceptions """

class BaseException(Exception):
    """Base class for other exceptions"""
    pass

class ValueTooLarge(BaseException):
    """Raised when the user enters country-code that is longer than 2 """
    #used this for testing userinput
    pass

class NoStateRegion(BaseException):
    """ Raised when the user state/region is not supported by API """
    pass