from __future__ import annotations

import os

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from textx import textx_isinstance
from textx.metamodel import TextXMetaModel

from wash_lang_prototype.core.options import WashOptions
from wash_lang_prototype.lang.wash import *


def create_executor_instance(script: str, options: WashOptions, metamodel: TextXMetaModel,
                             model: WashScript, debug=False, **kwargs):

    from wash_lang_prototype.core.configuration_handler import ChromeConfigurationHandler, FirefoxConfigurationHandler, EdgeConfigurationHandler, OperaConfigurationHandler
    chrome_handler = ChromeConfigurationHandler()
    firefox_handler = FirefoxConfigurationHandler()
    edge_handler = EdgeConfigurationHandler()
    opera_handler = OperaConfigurationHandler()

    # TODO (fivkovic): Handle case when no configuration is specified to use default one?
    chrome_handler.set_next(firefox_handler).set_next(edge_handler).set_next(opera_handler)

    result = chrome_handler.handle(model.configuration)

    return result.executor_type(browser_options=result.browser_options,
                                **dict(kwargs, script=script, options=options,
                                       metamodel=metamodel, model=model, debug=debug,
                                       implicit_wait_value=result.implicit_wait_value))

class WashExecutor:
    """
    Main class that handles execution logic of WASH scripts.
    """

    def __init__(self, **kwargs):
        self._options = kwargs.pop('options')                       # type: WashOptions
        self.__script = kwargs.pop('script')                        # type: str
        self.__metamodel = kwargs.pop('metamodel')                  # type: TextXMetaModel
        self.__model = kwargs.pop('model')                          # type: WashScript
        self.__debug = kwargs.pop('debug')                          # type: bool
        self._time_to_wait = kwargs.pop('implicit_wait_value')      # type: int

    def execute(self) -> ExecutionResult:
        """
        Executes a WASH script and returns an ExecutionResult instance.
        """
        document_location = self.__extract_document_location(self.__model.open_statement)
        webdriver_instance = self._start_webdriver_instance(url=document_location)
        
        execution_result = self.__execute_internal(webdriver_instance)
        
        wash_result = ExecutionResult(
            parent=None,
            start_url=document_location,
            current_url=webdriver_instance.current_url,
            execution_result=execution_result)
        
        webdriver_instance.quit()

        if self.__debug:
            wash_result.add_attributes(**{'script': self.__script})
        
        return wash_result

    def _start_webdriver_instance(self, url: str) -> WebDriver:
        """
        Starts a new webdriver instance on the given URL.
        
        Args:
            url(str): URL of the page the webdriver instance should load.
        """
        pass

    def __is(self, object_instance, rule_class):
        """
        Determines whether a WASH object is an instance of a specific WASH class supported by the metamodel.
        
        Args:
            object_instance: The object to be checked.
            rule_class: The class to be used for checking.
        Returns:
            True if object_instance is an instance of rule_class.
        """
        return textx_isinstance(object_instance, self.__metamodel[rule_class])

    def __extract_document_location(self, open_statement):
        """
        Extracts the location value of the document that should be used for execution,
        and returns it in a format acceptable by the WebDriver class.
        
        Args:
            open_statement: Statement from the parsed model that contains location value for opening a HTML file.
        """
        if self.__is(open_statement, OpenURLStatement.__name__):
            return open_statement.url
        elif self.__is(open_statement, OpenFileStatement.__name__):
            return 'file:///' + open_statement.file_path
        elif self.__is(open_statement, OpenStringStatement.__name__):
            return 'data:text/html;charset=utf-8,' + open_statement.html
        else:
            raise WashError('Unexpected object "{}" of type "{}"'.format(open_statement, type(open_statement)))
            
    def __execute_internal(self, webdriver_instance: WebDriver) -> ExecutionResult:
        for expression in self.__model.expressions:
            if self.__is(expression, DynamicExpression.__name__):
                expression.execute(webdriver_instance)
            elif self.__is(expression, StaticExpression.__name__):
                queries = expression.queries
                context_expression = expression.context_expression
                result_key = expression.result_key

                root_context = self.__prepare_context(webdriver_instance, queries)

                result = self.__execute_context_expression(root_context, context_expression)
                self.__model.execution_result[result_key] = result
            else:
                raise WashError(f'Unsupported expression type: {expression.__class__}')

        return self.__model.execution_result

    def __execute_context_expression(self, context: list[WebElement],
                                     context_expression: ContextExpression, parent=None):

        execution_result = []
        for context_item in context:                                            # Each web element in current context
            context_item_execution_result = ExecutionResult(parent=parent)

            for expression in context_expression.expressions:                   # Each expression to be executed on
                expression_queries = expression.queries                         # current context
                expression_context_expression = expression.context_expression
                expression_result_key = expression.result_key

                expression_result = None
                if expression_context_expression:
                    sub_context = self.__prepare_context(context_item, expression_queries)
                    expression_result = self.__execute_context_expression(sub_context, expression_context_expression,
                                                                          parent=execution_result)
                else:
                    for query in expression_queries:
                        if expression_result:
                            expression_result = query.execute(execution_context=expression_result)
                        else:
                            expression_result = query.execute(execution_context=context_item)

                context_item_execution_result.add_attributes(**{expression_result_key: expression_result})
            execution_result.append(context_item_execution_result)

        if len(execution_result) == 1:
            return execution_result[0]
        return execution_result

    @staticmethod
    def __prepare_context(execution_context: [WebElement or WebDriver], queries: list[Query]) -> list[WebElement]:
        query_result = None
        for query in queries:
            if not query_result:
                query_result = query.execute(execution_context=execution_context)
            else:
                query_result = query.execute(query_result)

        return query_result


class ChromeExecutor(WashExecutor):
    """
    WASH script executor that uses Chrome browser.
    """
    def __init__(self, browser_options, **kwargs):
        super(ChromeExecutor, self).__init__(**kwargs)
        self.__chrome_options = browser_options

    def _start_webdriver_instance(self, url: str):
        if not self._options.chrome_webdriver_path:
            raise WashError('Current WASH configuration uses Chrome WebDriver,'
                            ' but the path was not specified in options.')
        elif not os.path.exists(self._options.chrome_webdriver_path):
            raise FileNotFoundError('Unable to find Chrome WebDriver on specified path: "{}"'
                                    .format(self._options.chrome_webdriver_path))

        webdriver_instance = webdriver.Chrome(options=self.__chrome_options,
                                              executable_path=self._options.chrome_webdriver_path)
        webdriver_instance.implicitly_wait(time_to_wait=self._time_to_wait)
        webdriver_instance.get(url)

        return webdriver_instance


class FirefoxExecutor(WashExecutor):
    """
    WASH script executor that uses Firefox browser.
    """
    def __init__(self, browser_options, **kwargs):
        super(FirefoxExecutor, self).__init__(**kwargs)
        self.__firefox_options = browser_options

    def _start_webdriver_instance(self, url: str):
        if not self._options.firefox_webdriver_path:
            raise WashError('Current WASH configuration uses Firefox WebDriver,'
                            ' but the path was not specified in options.')
        elif not os.path.exists(self._options.firefox_webdriver_path):
            raise FileNotFoundError('Unable to find Firefox WebDriver on specified path: "{}"'
                                    .format(self._options.firefox_webdriver_path))

        webdriver_instance = webdriver.Firefox(options=self.__firefox_options,
                                               executable_path=self._options.firefox_webdriver_path)
        webdriver_instance.implicitly_wait(time_to_wait=self._time_to_wait)
        webdriver_instance.get(url)

        return webdriver_instance


class EdgeExecutor(WashExecutor):
    """
    WASH script executor that uses Edge browser.
    """
    def __init__(self, browser_options, **kwargs):
        super(EdgeExecutor, self).__init__(**kwargs)
        self.__edge_options = browser_options

    def _start_webdriver_instance(self, url: str):

        # TODO (fivkovic): Use additional library to set options
        # https://stackoverflow.com/questions/65171183/how-to-run-microsoft-edge-headless-with-selenium-python

        if not self._options.edge_webdriver_path:
            raise WashError('Current WASH configuration uses Edge WebDriver,'
                            ' but the path was not specified in options.')
        elif not os.path.exists(self._options.edge_webdriver_path):
            raise FileNotFoundError('Unable to find Edge WebDriver on specified path: "{}"'
                                    .format(self._options.edge_webdriver_path))

        webdriver_instance = webdriver.Edge(executable_path=self._options.edge_webdriver_path)
        webdriver_instance.implicitly_wait(time_to_wait=self._time_to_wait)
        webdriver_instance.get(url)

        return webdriver_instance


class OperaExecutor(WashExecutor):
    """
    WASH script executor that uses Opera browser.
    """
    def __init__(self, browser_options, **kwargs):
        super(OperaExecutor, self).__init__(**kwargs)
        self.__opera_options = browser_options

    def _start_webdriver_instance(self, url: str):
        if not self._options.opera_webdriver_path:
            raise WashError('Current WASH configuration uses Opera WebDriver,'
                            ' but the path was not specified in options.')
        elif not os.path.exists(self._options.opera_webdriver_path):
            raise FileNotFoundError('Unable to find Opera WebDriver on specified path: "{}"'
                                    .format(self._options.opera_webdriver_path))

        webdriver_instance = webdriver.Opera(options=self.__opera_options,
                                             executable_path=self._options.opera_webdriver_path)
        webdriver_instance.implicitly_wait(time_to_wait=self._time_to_wait)
        webdriver_instance.get(url)

        return webdriver_instance


class SafariExecutor(WashExecutor):
    """
    WASH script executor that uses Safari browser.
    """
    def __init__(self, browser_options, **kwargs):
        super(SafariExecutor, self).__init__(**kwargs)
        self.__safari_options = browser_options

    def _start_webdriver_instance(self, url: str):

        # TODO (fivkovic): Safari still does not support headless mode in 2021. Disable support for now.
        # Reference: https://github.com/SeleniumHQ/selenium/issues/5985

        if not self._options.safari_webdriver_path:
            raise WashError('Current WASH configuration uses Safari WebDriver,'
                            ' but the path was not specified in options.')
        elif not os.path.exists(self._options.safari_webdriver_path):
            raise FileNotFoundError('Unable to find Safari WebDriver on specified path: "{}"'
                                    .format(self._options.safari_webdriver_path))

        webdriver_instance = webdriver.Safari(executable_path=self._options.safari_webdriver_path)
        webdriver_instance.implicitly_wait(time_to_wait=self._time_to_wait)
        webdriver_instance.get(url)

        return webdriver_instance