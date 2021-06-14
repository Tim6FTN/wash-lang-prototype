
class WashOptions:
    """
    WashOptions is used to provide required locations of WebDriver executables
    used for WASH script execution and enables additional configuration of the WASH executor.
    """
    def __init__(self):
        self._chrome_webdriver_path = None
        self._firefox_webdriver_path = None
        self._edge_webdriver_path = None
        self._opera_webdriver_path = None
        self._safari_webdriver_path = None

    @property
    def chrome_webdriver_path(self) -> str:
        """ Gets the value of the currently set location of Google Chrome WebDriver executable """
        return self._chrome_webdriver_path

    @chrome_webdriver_path.setter
    def chrome_webdriver_path(self, value: str):
        """ Sets the path of the Google Chrome WebDriver executable to be used """
        self._chrome_webdriver_path = value

    @property
    def firefox_webdriver_path(self) -> str:
        """ Gets the value of the currently set location of Mozilla Firefox WebDriver executable """
        return self._firefox_webdriver_path

    @firefox_webdriver_path.setter
    def firefox_webdriver_path(self, value: str):
        """ Sets the path of the Mozilla Firefox WebDriver executable to be used """
        self._firefox_webdriver_path = value

    @property
    def edge_webdriver_path(self) -> str:
        """ Gets the value of the currently set location of Microsoft Edge WebDriver executable """
        return self._edge_webdriver_path

    @edge_webdriver_path.setter
    def edge_webdriver_path(self, value: str):
        """ Sets the path of the Microsoft Edge WebDriver executable to be used """
        self._edge_webdriver_path = value

    @property
    def opera_webdriver_path(self) -> str:
        """ Gets the value of the currently set location of Opera WebDriver executable """
        return self._opera_webdriver_path

    @opera_webdriver_path.setter
    def opera_webdriver_path(self, value: str):
        """ Sets the path of the Opera WebDriver executable to be used """
        self._opera_webdriver_path = value

    @property
    def safari_webdriver_path(self) -> str:
        """ Gets the value of the currently set location of Safari WebDriver executable """
        return self._safari_webdriver_path

    @safari_webdriver_path.setter
    def safari_webdriver_path(self, value: str):
        """ Sets the path of the Safari WebDriver executable to be used """
        self._safari_webdriver_path = value
