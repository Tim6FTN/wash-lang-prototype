import os
from typing import Any

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from textx.metamodel import TextXMetaModel

from wash_lang_prototype.core.options import WashOptions


def create_executor_instance(script: str, options: WashOptions, metamodel: TextXMetaModel,
                             model, debug=False, **kwargs):

    # TODO (fivkovic): Create executor based on current configuration.
    # Current configuration set in WASH script should contain what browser is to be used.

    return ChromeExecutor(**dict(kwargs, script=script, options=options,
                                 metamodel=metamodel, model=model, debug=debug))


class WashExecutor:
    def __init__(self, **kwargs):
        self._options = kwargs.pop('options')           # type: WashOptions
        self.__script = kwargs.pop('script')            # type: str
        self.__metamodel = kwargs.pop('metamodel')      # type: TextXMetaModel
        self.__model = kwargs.pop('model')
        self.__debug = kwargs.pop('debug')              # type: bool

    def execute(self) -> dict[str, Any]:
        return {}

    def _start_webdriver_instance(self, url: str) -> WebDriver:
        pass



class ChromeExecutor(WashExecutor):
    """
    WASH script executor that uses Chrome browser.
    """
    def __init__(self, **kwargs):
        super(ChromeExecutor, self).__init__(**kwargs)

    def _start_webdriver_instance(self, url: str):
        from selenium.webdriver import ChromeOptions

        options = ChromeOptions()
        options.headless = True
        options.add_argument("--window-size=1920,1080")

        if not os.path.exists(self._options.chrome_webdriver_path):
            raise FileNotFoundError('Unable to find Chrome WebDriver on specified path: "{}"'
                                    .format(self._options.chrome_webdriver_path))

        webdriver_instance = webdriver.Chrome(options=options, executable_path=self._options.chrome_webdriver_path)
        webdriver_instance.get(url)

        return webdriver_instance


class FirefoxExecutor(WashExecutor):
    """
    WASH script executor that uses Firefox browser.
    """
    def __init__(self, **kwargs):
        super(FirefoxExecutor, self).__init__(**kwargs)

    def _start_webdriver_instance(self, url: str):
        from selenium.webdriver import FirefoxOptions

        options = FirefoxOptions()
        options.headless = True
        options.add_argument("--window-size=1920,1080")

        if not os.path.exists(self._options.firefox_webdriver_path):
            raise FileNotFoundError('Unable to find Firefox WebDriver on specified path: "{}"'
                                    .format(self._options.firefox_webdriver_path))

        webdriver_instance = webdriver.Firefox(options=options, executable_path=self._options.firefox_webdriver_path)
        webdriver_instance.get(url)

        return webdriver_instance


class EdgeExecutor(WashExecutor):
    """
    WASH script executor that uses Edge browser.
    """
    def __init__(self, **kwargs):
        super(EdgeExecutor, self).__init__(**kwargs)

    def _start_webdriver_instance(self, url: str):

        # TODO (fivkovic): Use additional library to set options
        # https://stackoverflow.com/questions/65171183/how-to-run-microsoft-edge-headless-with-selenium-python

        if not os.path.exists(self._options.edge_webdriver_path):
            raise FileNotFoundError('Unable to find Edge WebDriver on specified path: "{}"'
                                    .format(self._options.edge_webdriver_path))

        webdriver_instance = webdriver.Edge(executable_path=self._options.edge_webdriver_path)
        webdriver_instance.get(url)

        return webdriver_instance


class OperaExecutor(WashExecutor):
    """
    WASH script executor that uses Opera browser.
    """
    def __init__(self, **kwargs):
        super(OperaExecutor, self).__init__(**kwargs)

    def _start_webdriver_instance(self, url: str):
        from selenium.webdriver.opera.options import Options

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")

        if not os.path.exists(self._options.opera_webdriver_path):
            raise FileNotFoundError('Unable to find Opera WebDriver on specified path: "{}"'
                                    .format(self._options.opera_webdriver_path))

        webdriver_instance = webdriver.Opera(options=options, executable_path=self._options.opera_webdriver_path)
        webdriver_instance.get(url)

        return webdriver_instance


class SafariExecutor(WashExecutor):
    """
    WASH script executor that uses Safari browser.
    """
    def __init__(self, **kwargs):
        super(SafariExecutor, self).__init__(**kwargs)

    def _start_webdriver_instance(self, url: str):

        # TODO: Safari still does not support headless mode in 2021. Disable support for now and check what to do.
        # Reference: https://github.com/SeleniumHQ/selenium/issues/5985

        if not os.path.exists(self._options.safari_webdriver_path):
            raise FileNotFoundError('Unable to find Safari WebDriver on specified path: "{}"'
                                    .format(self._options.safari_webdriver_path))

        webdriver_instance = webdriver.Safari(executable_path=self._options.safari_webdriver_path)
        webdriver_instance.get(url)

        return webdriver_instance