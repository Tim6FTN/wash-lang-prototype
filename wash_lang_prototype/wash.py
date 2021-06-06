import codecs
import json
import os

from textx import metamodel_for_language

from wash_lang_prototype.core.exceptions import WashError
from wash_lang_prototype.core.executor import WashExecutor, create_executor_instance, ExecutionResult
from wash_lang_prototype.core.options import WashOptions


class Wash:
    def __init__(self, **kwargs):
        self.__executor = kwargs.pop('executor')                    # type: WashExecutor

    @staticmethod
    def from_file(script_file_path: str, options: WashOptions, encoding: str = 'utf-8', debug=False, **kwargs):
        """
        Creates a new executable WASH instance.

        Args:
            script_file_path(str): The path of the WASH script file.
            options(WashOptions): Instance of WashOptions that enables configuration of the WASH executor.
            encoding(str): The encoding to be used for reading the contents of the WASH script file.
            debug(bool): Indicates whether debug messages should be printed or not.
        """

        script_file_path = os.path.abspath(script_file_path)
        with codecs.open(script_file_path, 'r', encoding) as script_file:
            script = script_file.read()

        return Wash.from_string(script=script, options=options, encoding=encoding,
                                script_file_path=script_file_path, debug=debug, **kwargs)

    @staticmethod
    def from_string(script: str, options: WashOptions, encoding: str = 'utf-8',
                    script_file_path=None, debug=False, **kwargs):
        """
        Creates a new executable WASH instance.

        Args:
            script(str): The contents of the WASH script.
            options(WashOptions): Instance of WashOptions that enables configuration of the WASH executor.
            encoding(str): The encoding to be used for reading the contents of the WASH script file.
            script_file_path(str): The path of the WASH script file.
            debug(bool): Indicates whether debug messages should be printed or not.
        """

        if type(script) is not str:
            raise WashError("Invalid script format: only UTF-8 encoded scripts are supported.")

        return Wash.__create_instance(script=script, options=options, encoding=encoding,
                                      script_file_path=script_file_path, debug=debug, **kwargs)

    @staticmethod
    def __create_instance(script: str, options: WashOptions, encoding: str = 'utf-8',
                          script_file_path=None, debug=False, **kwargs):
        """
        Creates a new executable WASH instance.

        Args:
            script(str): The contents of the WASH script.
            options(WashOptions): Instance of WashOptions that enables configuration of the WASH executor.
            encoding(str): The encoding to be used for reading the contents of the WASH script file.
            debug(bool): Indicates whether debug messages should be printed or not.
        """
        metamodel = metamodel_for_language('wash')
        model = metamodel.model_from_str(script, encoding=encoding, file_name=script_file_path, debug=debug)

        # NOTE: Providing the filename as parameter is required as a workaround
        # for using model_from_str having _tx_filename set at the same time.

        executor = create_executor_instance(script=script, options=options, metamodel=metamodel,
                                            model=model, debug=debug, **kwargs)

        return Wash(executor=executor)

    def execute(self) -> ExecutionResult:
        """
        Executes the WASH script and returns the execution result in form of a dictionary.
        """
        return self.__executor.execute()

    def execute_as_json(self) -> str:
        """
        Executes the WASH script and returns the execution result as a JSON string value.
        """
        return json.dumps(self.__executor.execute())