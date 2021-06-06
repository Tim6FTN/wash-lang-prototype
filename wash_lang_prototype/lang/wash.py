

class WashScript:
    def __init__(self, configuration_definitions, import_statements, configuration, open_statement, root_expression):
        self.configuration_definitions = configuration_definitions
        self.import_statements = import_statements
        self.configuration = configuration
        self.open_statement = open_statement
        self.root_expression = root_expression
        self.execution_result = {}


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


class CSSSelectorQuery(Query):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)
        self.execution_result = None


class XPathSelectorQuery(Query):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)
        self.execution_result = None


class DataQuery(Query):
    def __init__(self, parent, query_value):
        super().__init__(parent, query_value)
        self.execution_result = None


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
    OpenURLStatement, OpenFileStatement, OpenStringStatement,
    Expression, ContextExpression, 
    CSSSelectorQuery, XPathSelectorQuery, DataQuery,
    QueryValue
]