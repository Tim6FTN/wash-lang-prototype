import itertools
import re
import time
from abc import abstractmethod
from typing import Any

from wash_lang_prototype.core.exceptions import WashRuntimeError, WashLanguageError
from wash_lang_prototype.core.result import ExecutionResult


class WashBase:
    """
    Represents the base class for all custom classes used during the meta-model instantiation.
    """
    def __init__(self, *args, **kwargs):
        if args:
            self.parent = args[0]
        for key, item in kwargs.items():
            setattr(self, key, item)
        super().__init__()


class WashScript(WashBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execution_result = ExecutionResult()


class ConfigurationParameterValue(WashBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConfigurationEntry(WashBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def extract_parameter_value(self, parameter_name: str) -> Any:
        """
        Extracts the parameter value by given name from current ConfigurationEntry instance.
        In case the parameter with given name is not found, a WashLanguageError is raised.

        Args:
            parameter_name(str): Name of the parameter in the entry.
        """
        parameter_value = next(parameter.value.value for parameter in self.parameters
                               if parameter.parameter.name == parameter_name)
        if parameter_value is None:
            raise WashLanguageError(f'Parameter {parameter_name} does not exist '
                                    f'in configuration entry "{self.type.name}".')

        return parameter_value


class Configuration(WashBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __extract_configuration_entry(self, entry_name: str) -> [ConfigurationEntry, None]:
        """
        Extracts configuration entry by given name from current Configuration instance.
        In case the entry with given name is not found, a None value is returned.

        Args:
            entry_name(str): Name of the configuration entry.
        """
        try:
            return next(entry for entry in self.configuration_entries if entry.type.name == entry_name)
        except StopIteration:
            return None

    def __extract_configuration_entry_value(self, entry_name: str, value_name: str):
        entry = self.__extract_configuration_entry(entry_name)
        return entry if not entry else entry.extract_parameter_value(value_name)

    def get_browser_type(self) -> [str, None]:
        """
        Extracts 'browser type' configuration value from given configuration.
        """
        return self.__extract_configuration_entry_value('browser_type', 'browser_type')

    def get_user_agent(self) -> [str, None]:
        """
        Extracts 'user agent' configuration value from given configuration.
        """
        return self.__extract_configuration_entry_value('user_agent', 'user_agent')

    def get_access_as_mobile_device(self) -> [bool, None]:
        """
        Extracts 'access as mobile device' configuration value from given configuration.
        """
        return self.__extract_configuration_entry_value('access_as_mobile_device', 'is_active')

    def get_use_incognito_mode(self) -> [bool, None]:
        """
        Extracts 'use incognito mode' configuration value from given configuration.
        """
        return self.__extract_configuration_entry_value('use_incognito_mode', 'is_active')

    def get_window_size(self) -> [tuple[int, int], None]:
        """
        Extracts 'window size' configuration value from given configuration.
        """
        width_value = self.__extract_configuration_entry_value('window_size', 'width')
        height_value = self.__extract_configuration_entry_value('window_size', 'height')

        return None if not width_value or not height_value else (width_value, height_value)

    def get_wait_timeout(self) -> [int, None]:
        """
        Extracts 'wait timeout' configuration value from given configuration.
        """
        return self.__extract_configuration_entry_value('wait_timeout', 'timeout')

    def get_cookies(self) -> [dict[str, str], None]:
        """
        Extracts 'cookies' configuration value from given configuration.
        """
        cookie_names = self.__extract_configuration_entry_value('cookies', 'cookie_names')
        cookie_values = self.__extract_configuration_entry_value('cookies', 'cookie_values')

        return None if not cookie_names or not cookie_values else dict(zip(cookie_names, cookie_values))


class OpenURLStatement(WashBase):
    def __init__(self, parent, url):
        super().__init__(parent)
        self.url = url


class OpenFileStatement(WashBase):
    def __init__(self, parent, file_path):
        super().__init__(parent)
        self.file_path = file_path


class OpenStringStatement(WashBase):
    def __init__(self, parent, html):
        super().__init__(parent)
        self.html = html


class StaticExpression(WashBase):
    def __init__(self, parent, queries, context_expression, result_key):
        super().__init__(parent)
        self.queries = queries
        self.context_expression = context_expression
        self.result_key = result_key
        self.execution_context = None                       # TODO: Use execution_context
    

class Query(WashBase):
    def __init__(self, parent, query_value):
        super().__init__(parent)
        self.query_value = query_value

    def execute(self, execution_context):
        if isinstance(execution_context, list):
            if len(execution_context) == 1:
                return self._execute(execution_context[0])
            else:
                return self._execute_and_flatten(execution_context)
        else:
            return self._execute(execution_context)

    @abstractmethod
    def _execute(self, execution_context):
        raise NotImplementedError(f"Calling this method from {__class__} class is not allowed.")

    @abstractmethod
    def _execute_and_flatten(self, execution_context: list):
        raise NotImplementedError(f"Calling this method from {__class__} class is not allowed.")


class SelectorQuery(Query):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)

    def execute(self, execution_context):
        if not self._execution_context_valid(execution_context):
            raise ValueError(f"{__class__}: Unsupported execution context type {execution_context.__class__}.")

        if isinstance(execution_context, list):
            if len(execution_context) == 1:
                return self._execute(execution_context[0])
            else:
                return self._execute_and_flatten(execution_context)
        else:
            return self._execute(execution_context)

    def _execution_context_valid(self, execution_context) -> bool:
        return True

    @abstractmethod
    def _execute(self, execution_context):
        raise NotImplementedError(f"Calling this method from {__class__} class is not allowed.")

    @abstractmethod
    def _execute_and_flatten(self, execution_context):
        raise NotImplementedError(f"Calling this method from {__class__} class is not allowed.")

    @abstractmethod
    def _execute_selector(self, execution_context):
        raise NotImplementedError(f"Calling this method from {__class__} class is not allowed.")


class IndexSelectorQuery(SelectorQuery):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)

    def execute(self, execution_context):
        # NOTE: This method is overridden because
        #       different behavior is expected for IndexSelectorQuery compared to all other selector queries.
        if not isinstance(execution_context, list):
            execution_context = [execution_context]

        return self._execute(execution_context)

    def _execution_context_valid(self, execution_context):
        return isinstance(execution_context, list)

    def _execute(self, execution_context: list):
        if not self._execution_context_valid(execution_context):
            raise ValueError(f"{__class__}: Unsupported execution context type {execution_context.__class__}.")

        return self._execute_selector(execution_context)

    def _execute_and_flatten(self, execution_context: list) -> list:
        raise NotImplementedError(f"Calling this method from {__class__} class is not allowed.")

    def _execute_selector(self, execution_context):
        # TODO (fivkovic): Add first n items feature
        if re.match(r"[-+]?\d+$", self.query_value.value) is None:
            raise WashLanguageError(f"Index selector value is not an integer value: {self.query_value.value}.")

        index = int(self.query_value.value)
        if abs(index) == 0:
            raise WashRuntimeError(f"Index selector value is not valid: {self.query_value.value}.")
        if abs(index) > len(execution_context):
            raise WashRuntimeError(f"Index accessor value out of range: "
                                   f"given value {index} exceeds collection size ({len(execution_context)}).")

        """
        NOTE: 
            Negative value refers to skipping given number of items. 
            Positive value refers to selecting single item on given index. 
        """
        selector_result = execution_context[index - 1] if index > 0 else execution_context[-index:]

        return selector_result if isinstance(selector_result, list) else [selector_result]


class IDSelectorQuery(SelectorQuery):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)

    def _execute(self, execution_context):
        return self._execute_selector(execution_context)

    def _execute_and_flatten(self, execution_context: list) -> list:
        result = [self._execute_selector(execution_item) for execution_item in execution_context]
        return list(itertools.chain.from_iterable(result))

    def _execute_selector(self, execution_context):
        return execution_context.find_element_by_id(self.query_value.value)


class NameSelectorQuery(SelectorQuery):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)

    def _execute(self, execution_context):
        return self._execute_selector(execution_context)

    def _execute_and_flatten(self, execution_context: list) -> list:
        result = [self._execute_selector(execution_item) for execution_item in execution_context]
        return list(itertools.chain.from_iterable(result))

    def _execute_selector(self, execution_context):
        return execution_context.find_elements_by_name(self.query_value.value)


class TagSelectorQuery(SelectorQuery):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)

    def _execute(self, execution_context):
        return self._execute_selector(execution_context)

    def _execute_and_flatten(self, execution_context: list) -> list:
        result = [self._execute_selector(execution_item) for execution_item in execution_context]
        return list(itertools.chain.from_iterable(result))

    def _execute_selector(self, execution_context):
        return execution_context.find_elements_by_tag_name(self.query_value.value)


class ClassSelectorQuery(SelectorQuery):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)

    def _execute(self, execution_context):
        return self._execute_selector(execution_context)

    def _execute_and_flatten(self, execution_context: list) -> list:
        result = [self._execute_selector(execution_item) for execution_item in execution_context]
        return list(itertools.chain.from_iterable(result))

    def _execute_selector(self, execution_context):
        return execution_context.find_elements_by_class_name(self.query_value.value)


class CSSSelectorQuery(SelectorQuery):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)

    def _execute(self, execution_context):
        return self._execute_selector(execution_context)

    def _execute_and_flatten(self, execution_context: list) -> list:
        result = [self._execute_selector(execution_item) for execution_item in execution_context]
        return list(itertools.chain.from_iterable(result))

    def _execute_selector(self, execution_context):
        return execution_context.find_elements_by_css_selector(self.query_value.value)


class XPathSelectorQuery(SelectorQuery):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)

    def _execute(self, execution_context):
        return self._execute_selector(execution_context)

    def _execute_and_flatten(self, execution_context: list) -> list:
        result = [self._execute_selector(execution_item) for execution_item in execution_context]
        return list(itertools.chain.from_iterable(result))

    def _execute_selector(self, execution_context):
        return execution_context.find_elements_by_xpath(self.query_value.value)


class DataQuery(Query):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)

    def _execute(self, execution_context):
        return self.__execute_data_query(execution_context)

    def _execute_and_flatten(self, execution_context: list) -> list:
        return [self.__execute_data_query(execution_item) for execution_item in execution_context]

    def __execute_data_query(self, execution_item):
        if self.query_value.value == 'text':
            return execution_item.text
        elif self.query_value.value == 'html':
            return execution_item.get_attribute('outerHTML')
        elif self.query_value.value == 'inner_html':
            return execution_item.get_attribute('innerHTML')
        elif self.query_value.value[0] == '@':
            attribute_name = self.query_value.value[1:]
            return execution_item.get_attribute(attribute_name)
        else:
            raise ValueError(f'Unsupported DataQuery value: {self.query_value.value}')


class QueryValue(WashBase):
    def __init__(self, parent, value):
        super().__init__(parent)
        self.value = value.strip()


class ContextExpression(WashBase):
    def __init__(self, parent, expressions):
        super().__init__(parent)
        self.expressions = expressions
        self.execution_result = None


class DynamicExpression(WashBase):
    def __init__(self, parent):
        super().__init__(parent)


class MouseEventCommand(DynamicExpression):
    def __init__(self, parent, element_selector_queries):
        super().__init__(parent)
        self.element_selector_queries = element_selector_queries

    def execute(self, execution_context):
        element_to_click = self.__get_element_to_click(execution_context)
        element_to_click = element_to_click[0] if isinstance(element_to_click, list) else element_to_click
        element_to_click.click()

    def __get_element_to_click(self, execution_context):
        query_result = None
        for query in self.element_selector_queries:
            if not query_result:
                query_result = query.execute(execution_context=execution_context)
            else:
                query_result = query.execute(query_result)

        return query_result


class ScriptExecutionCommand(DynamicExpression):
    def __init__(self, parent, script):
        super().__init__(parent)
        self.script = script

    def execute(self, execution_context):
        # TODO: Raise exception if not a web driver instance
        execution_context.execute_script(self.script)


class KeyboardEventCommand(DynamicExpression):
    def __init__(self, parent, value, element_selector_queries=None):
        super().__init__(parent)
        self.value = value
        self.element_selector_queries = element_selector_queries

    def execute(self, execution_context):
        if not self.element_selector_queries:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(execution_context)
            actions.send_keys(self.value)
            actions.perform()
        else:
            element_to_type = self.__get_element_to_type(execution_context)
            element_to_type = element_to_type[0] if isinstance(element_to_type, list) else element_to_type
            element_to_type.clear()
            element_to_type.send_keys(self.value)

    def __get_element_to_type(self, execution_context):
        query_result = None
        for query in self.element_selector_queries:
            if not query_result:
                query_result = query.execute(execution_context=execution_context)
            else:
                query_result = query.execute(query_result)

        return query_result


class SleepCommand(DynamicExpression):
    def __init__(self, parent, value):
        super().__init__(parent)
        self.value = value

    def execute(self, _):
        time.sleep(self.value)


class ExplicitWaitCommand(DynamicExpression):
    def __init__(self, parent, selector_query, rule, timeout_value=None):
        super().__init__(parent)
        self.parent = parent
        self.selector_query = selector_query
        self.rule = rule
        self.timeout_value = timeout_value

    def execute(self, execution_context):
        pass        # TODO: Implement


class NavigationCommand(DynamicExpression):
    def __init__(self, parent, url):
        super().__init__(parent)
        self.url = url

    def execute(self, execution_context):
        # TODO: Raise exception if not a web driver instance
        execution_context.get(self.url)


wash_classes = [
    WashScript,
    Configuration, ConfigurationEntry, ConfigurationParameterValue,
    OpenURLStatement, OpenFileStatement, OpenStringStatement,
    StaticExpression, ContextExpression, 
    IndexSelectorQuery, IDSelectorQuery, NameSelectorQuery, TagSelectorQuery, ClassSelectorQuery,
    CSSSelectorQuery, XPathSelectorQuery, 
    DataQuery,
    QueryValue,
    MouseEventCommand, ScriptExecutionCommand, KeyboardEventCommand,
    SleepCommand, ExplicitWaitCommand, NavigationCommand
]
