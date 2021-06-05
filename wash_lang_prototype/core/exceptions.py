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

        return ('WashError: {{\n'
                '       message: {!r}\n'
                '}}'
                ).format(self.__message)
