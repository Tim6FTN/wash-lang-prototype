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

