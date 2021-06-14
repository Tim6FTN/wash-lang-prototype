from typing import Optional


class WashError(Exception):
    """
    General purpose error class in WASH.
    """

    def __init__(self, message: Optional[str] = None):
        super(WashError, self).__init__(message.encode('utf-8'))

        self.__message = message

    def __str__(self):
        if not self.__message:
            return super(WashError, self).__str__()

        return ('{!r}: {{\n'
                '       message: {!r}\n'
                '}}'
                ).format(self.__class__.__name__, self.__message)


class WashLanguageError(WashError):
    """
    Represents a specific error class related to WASH language errors.
    """

    def __init__(self, message):
        super(WashLanguageError, self).__init__(message)


class WashRuntimeError(WashError):
    """
    Represents a specific error class related to WASH runtime errors.
    """

    def __init__(self, message):
        super(WashRuntimeError, self).__init__(message)
