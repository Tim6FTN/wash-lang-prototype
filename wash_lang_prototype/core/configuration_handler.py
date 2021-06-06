from __future__ import annotations

from abc import abstractmethod
from typing import Any, Type

from wash_lang_prototype.core.common import Handler
from wash_lang_prototype.core.exceptions import WashError
from wash_lang_prototype.core.executor import ChromeExecutor, FirefoxExecutor, EdgeExecutor, OperaExecutor
from wash_lang_prototype.lang.wash import Configuration


class ConfigurationHandler(Handler):
    """
    A base configuration handler implementing the default chaining behavior.
    """

    _next_configuration_handler: ConfigurationHandler = None

    def set_next(self, configuration_handler: ConfigurationHandler) -> ConfigurationHandler:
        self._next_configuration_handler = configuration_handler

        return configuration_handler

    @abstractmethod
    def handle(self, configuration: Configuration) -> tuple[Any, Any]:
        if self._next_configuration_handler:
            return self._next_configuration_handler.handle(configuration)

        raise WashError('Unsupported browser type')

    @classmethod
    def _extract_browser_type(cls, configuration: Configuration) -> str:
        browser_type_configuration_entry = next(entry for entry in configuration.configuration_entries
                                                if entry.type.name == 'browser_type')
        browser_type = next(parameter.value.value for parameter in browser_type_configuration_entry.parameters
                            if parameter.parameter.name == 'browser_type')

        return browser_type

    @abstractmethod
    def _create_options(self, configuration: Configuration):
        pass


class ChromeHandler(ConfigurationHandler):
    def handle(self, configuration: Configuration) -> tuple[Type[ChromeExecutor], Any]:
        browser_type = self._extract_browser_type(configuration)
        if browser_type == "Chrome":
            return ChromeExecutor, self._create_options(configuration)
        else:
            return super().handle(configuration)

    def _create_options(self, configuration: Configuration):
        from selenium.webdriver import ChromeOptions

        # TODO (fivkovic): Connect options and config.

        options = ChromeOptions()
        options.headless = True
        options.add_argument("--window-size=1920,1080")

        return options


class FirefoxHandler(ConfigurationHandler):
    def handle(self, configuration: Configuration) -> tuple[Type[FirefoxExecutor], Any]:
        browser_type = self._extract_browser_type(configuration)
        if browser_type == "Firefox":
            return FirefoxExecutor, self._create_options(configuration)
        else:
            return super().handle(configuration)

    def _create_options(self, configuration: Configuration):
        from selenium.webdriver import FirefoxOptions

        # TODO (fivkovic): Connect options and config.

        options = FirefoxOptions()
        options.headless = True
        options.add_argument("--window-size=1920,1080")

        return options


class EdgeHandler(ConfigurationHandler):
    def handle(self, configuration: Configuration) -> tuple[Type[EdgeExecutor], Any]:
        browser_type = self._extract_browser_type(configuration)
        if browser_type == "Edge":
            return EdgeExecutor, self._create_options(configuration)
        else:
            return super().handle(configuration)

    def _create_options(self, configuration: Configuration):

        # TODO (fivkovic): Use additional library to set options
        # https://stackoverflow.com/questions/65171183/how-to-run-microsoft-edge-headless-with-selenium-python

        # TODO (fivkovic): Connect options and config.

        return None


class OperaHandler(ConfigurationHandler):
    def handle(self, configuration: Configuration) -> tuple[Type[OperaExecutor], Any]:
        browser_type = self._extract_browser_type(configuration)
        if browser_type == "Opera":
            return OperaExecutor, self._create_options(configuration)
        else:
            return super().handle(configuration)

    def _create_options(self, configuration: Configuration):
        from selenium.webdriver.opera.options import Options

        # TODO (fivkovic): Connect options and config.

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")

        return None