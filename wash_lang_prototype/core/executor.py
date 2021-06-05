from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from textx import textx_isinstance
from textx.metamodel import TextXMetaModel

from wash_lang_prototype.core.exceptions import WashError
from wash_lang_prototype.core.options import WashOptions
from wash_lang_prototype.lang.wash import *


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
        document_location = self.__extract_document_location(self.__model.open_statement)
        webdriver_instance = self._start_webdriver_instance(url=document_location)

        execution_result = self.__execute_internal(webdriver_instance)

        wash_result = {
            'start_url': document_location,
            'current_url': webdriver_instance.current_url,
            'execution_result': execution_result
        }

        if self.__debug:
            wash_result['script'] = self.__script
        webdriver_instance.quit()

        return wash_result

    def _start_webdriver_instance(self, url: str) -> WebDriver:
        pass

    def _is(self, object_instance, rule_class):
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
        if self._is(open_statement, OpenURLStatement.__name__):
            return open_statement.url
        elif self._is(open_statement, OpenFileStatement.__name__):
            return 'file:///' + open_statement.file_path
        elif self._is(open_statement, OpenStringStatement.__name__):
            return 'data:text/html;charset=utf-8,' + open_statement.html
        else:
            raise WashError('Unexpected object "{}" of type "{}"'.format(open_statement, type(open_statement)))

    def __execute_internal(self, webdriver_instance: WebDriver) -> dict[str, Any]:

        root_expression_queries = self.__model.root_expression.queries
        root_expression_context_definition = self.__model.root_expression.context
        root_expression_result_key = self.__model.root_expression.result_key

        prepared_root_context = self.__prepare_root_context(webdriver_instance, root_expression_queries)

        result = self.__execute_sub_context(prepared_root_context, root_expression_context_definition)
        self.__model.execution_result[root_expression_result_key] = result

        return self.__model.execution_result

    def __prepare_root_context(self, web_driver_instance: WebDriver, root_expression_queries: list) -> list[WebElement]:

        root_context = None
        for query in root_expression_queries:
            if query.query_type_identifier == '?c':
                if not root_context:
                    root_context = web_driver_instance.find_elements_by_css_selector(query.query.query_value)
                else:
                    root_context = root_context.find_elements_by_css_selector(query.query.query_value)
            elif query.query_type_identifier == '?x':
                if not root_context:
                    root_context = web_driver_instance.find_elements_by_xpath(query.query.query_value)
                else:
                    root_context = root_context.find_elements_by_xpath(query.query.query_value)
            else:
                raise NotImplementedError(f'Unknown/unsupported root context query type: {query.query_type_identifier}')

        return root_context

    def __prepare_context(self, instance, expression_queries: list) -> list[WebElement]:

        if isinstance(instance, list):
            instance = instance[0]

        query_result = None
        for query in expression_queries:
            if query.query_type_identifier == '?c':
                if not query_result:
                    query_result = instance.find_elements_by_css_selector(query.query.query_value)
                else:
                    query_result = query_result.find_elements_by_css_selector(query.query.query_value)
            elif query.query_type_identifier == '?x':
                if not query_result:
                    query_result = instance.find_elements_by_xpath(query.query.query_value)
                else:
                    query_result = query_result.find_elements_by_xpath(query.query.query_value)
            else:
                raise NotImplementedError(f'Unknown/unsupported root context query type: {query.query_type_identifier}')

        return query_result

    def __execute_sub_context(self, context, context_definition):

        if not isinstance(context, list):
            context = [context]

        execution_result = []
        for context_item in context:
            context_item_execution_result = {}
            for expression in context_definition.expressions:
                expression_queries = expression.queries
                expression_context_definition = expression.context
                expression_result_key = expression.result_key

                temp_result = None
                if expression_context_definition:
                    sub_ctx_input = self.__prepare_context(context_item, expression_queries)
                    temp_result = self.__execute_sub_context(sub_ctx_input, expression_context_definition)
                else:
                    for query in expression_queries:
                        if temp_result:
                            temp_result = self.__execute_query_return_context(query, temp_result)
                        else:
                            temp_result = self.__execute_query_return_context(query, context_item)

                context_item_execution_result[expression_result_key] = temp_result
            execution_result.append(context_item_execution_result)

        return execution_result

    def __execute_query_return_context(self, query, context_to_execute_on):

        if not isinstance(context_to_execute_on, list):
            context_to_execute_on = [context_to_execute_on]

        for context_item in context_to_execute_on:
            if query.query_type_identifier == '?c':
                return context_item.find_elements_by_css_selector(query.query.query_value)
            elif query.query_type_identifier == '?x':
                return context_item.find_elements_by_xpath(query.query.query_value)
            elif query.query_type_identifier == ':':
                if query.query.query_value == 'text':
                    return context_item.text
                elif query.query.query_value == 'html':
                    return context_item.get_attribute('outerHTML')
                elif query.query.query_value == 'inner_html':
                    return context_item.get_attribute('innerHTML')
                else:
                    return context_item.get_attribute(query.query.query_value[1:])
            else:
                raise NotImplementedError(f'Unknown query type: {query.query_type_identifier}')


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