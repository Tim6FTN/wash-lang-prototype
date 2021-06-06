import itertools
import re

from wash_lang_prototype.core.exceptions import WashError
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

    # TODO (fivkovic): Scope, Context


class WashScript(WashBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execution_result = ExecutionResult()


class Configuration(WashBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.__is_valid():
            raise WashError('Configuration invalid: not all required parameters were specified.')

    # noinspection PyUnresolvedReferences
    def __is_valid(self):
        for e in self.configuration_entries:
            required_parameters = [p for p in e.type.parameters if p.required]
            if len(required_parameters) != len(e.parameters):
                return False
        return True


class ConfigurationEntry(WashBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConfigurationParameterValue(WashBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OpenStatement:
    def __init__(self, parent):
        self.parent = parent


class OpenURLStatement(OpenStatement):
    def __init__(self, parent, url):
        super().__init__(parent)
        self.url = url


class OpenFileStatement(OpenStatement):
    def __init__(self, parent, file_path):
        super().__init__(parent)
        self.file_path = file_path


class OpenStringStatement(OpenStatement):
    def __init__(self, parent, html):
        super().__init__(parent)
        self.html = html


class Expression:
    def __init__(self, parent, queries, context_expression, result_key):
        self.parent = parent
        self.queries = queries
        self.context_expression = context_expression
        self.result_key = result_key
        self.execution_context = None
    

class Query:
    def __init__(self, parent, query_value):
        self.parent = parent
        self.query_value = query_value

    def execute(self, execution_context):
        if isinstance(execution_context, list):
            if len(execution_context) == 1:
                return self._execute(execution_context[0])
            else:
                return self._execute_and_flatten(execution_context)
        else:
            return self._execute(execution_context)

    def _execute(self, execution_context):
        raise NotImplementedError(f"Calling this method from {__class__} class is not allowed.")

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

    def _execute(self, execution_context):
        raise NotImplementedError(f"Calling this method from {__class__} class is not allowed.")

    def _execute_and_flatten(self, execution_context):
        raise NotImplementedError(f"Calling this method from {__class__} class is not allowed.")

    def _execute_selector(self, execution_context):
        raise NotImplementedError(f"Calling this method from {__class__} class is not allowed.")


class IndexSelectorQuery(SelectorQuery):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)

    def _execution_context_valid(self, execution_context):
        return isinstance(execution_context, list)

    def _execute(self, execution_context):
        return self._execute_selector(execution_context)

    def _execute_and_flatten(self, execution_context: list) -> list:
        result = [self._execute_selector(execution_item) for execution_item in execution_context]
        return list(itertools.chain.from_iterable(result))

    def _execute_selector(self, execution_context):
        # TODO (fivkovic): Add first n items feature
        if re.match(r"[-+]?\d+$", self.query_value.value) is None:
            raise ValueError(f"Index selector value is not an integer value: {self.query_value.value}.")

        index = int(self.query_value.value)
        if abs(index) == 0:
            raise ValueError(f"Index selector value is not valid: {self.query_value.value}.")
        if abs(index) > execution_context.count:
            raise ValueError(f"Index accessor value out of range: "
                             f"given value {index} exceeds collection size ({execution_context.count}).")

        return list(execution_context[index - 1]) if index > 0 else execution_context[-index:]


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


class QueryValue:
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value.strip()


class ContextExpression:
    def __init__(self, parent, expressions):
        self.parent = parent
        self.expressions = expressions
        self.execution_result = None


wash_classes = [
    WashScript,
    Configuration, ConfigurationEntry, ConfigurationParameterValue,
    OpenURLStatement, OpenFileStatement, OpenStringStatement,
    Expression, ContextExpression, 
    IndexSelectorQuery, IDSelectorQuery, NameSelectorQuery, TagSelectorQuery, ClassSelectorQuery,
    CSSSelectorQuery, XPathSelectorQuery, 
    DataQuery,
    QueryValue
]