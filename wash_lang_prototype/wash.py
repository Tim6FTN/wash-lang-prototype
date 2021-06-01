import codecs
import os

from textx import metamodel_from_file

from wash_lang_prototype.core.exceptions import WashError


class Wash:
    def __init__(self, **kwargs):
        self.__webdriver_path = kwargs.pop('webdriver_path')
        self.__script = kwargs.pop('script')
        self.__metamodel = kwargs.pop('metamodel')
        self.__model = kwargs.pop('model')
        self.__debug = kwargs.pop('debug')

    @staticmethod
    def from_file(webdriver_path: str, script_file_path: str, encoding='utf-8', debug=False, **kwargs):
        """
        Creates a new executable WASH instance.
        Args:
            webdriver_path(str): The path of the WebDriver executable file.
            script_file_path(str): The path of the WASH script file.
            encoding(str): The encoding to be used for reading the contents of the WASH script file.
            debug(bool): Indicates whether debug messages should be printed or not.
        """

        script_file_path = os.path.abspath(script_file_path)
        with codecs.open(script_file_path, 'r', encoding) as script_file:
            script = script_file.read()

        return Wash.from_string(webdriver_path=webdriver_path, script=script,
                                encoding=encoding, debug=debug, **kwargs)

    @staticmethod
    def from_string(webdriver_path: str, script: str, encoding='utf-8', debug=False, **kwargs):
        """
        Creates a new executable WASH instance.
        Args:
            webdriver_path(str): The path of the WebDriver executable file.
            script(str): The contents of the WASH script.
            encoding(str): The encoding to be used for reading the contents of the WASH script file.
            debug(bool): Indicates whether debug messages should be printed or not.
        """

        if type(script) is not str:
            raise WashError("Invalid script format: only UTF-8 encoded scripts are supported.")

        return Wash.__create_instance(webdriver_path=webdriver_path, script=script,
                                      encoding=encoding, debug=debug, **kwargs)

    @staticmethod
    def __create_instance(webdriver_path: str, script: str, encoding='utf-8', debug=False, **kwargs):
        # TODO (fivkovic): Re-visit this to verify that it works as a package.
        path_to_metamodel = os.path.join(os.getcwd(), 'lang', 'wash.tx')

        metamodel = metamodel_from_file(path_to_metamodel, debug=debug)
        model = metamodel.model_from_str(script, encoding=encoding, debug=debug)

        return Wash(**dict(kwargs, webdriver_path=webdriver_path, script=script,
                           metamodel=metamodel, model=model, debug=debug))