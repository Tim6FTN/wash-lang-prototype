import os

from wash_lang_prototype.core.options import WashOptions
from wash_lang_prototype.wash import Wash

try:
    import click
except ImportError:
    raise Exception('Missing CLI dependencies. To use WASH from CLI, please run following command:/n'
                    'pip install wash-lang-prototype[cli]')


def execute(wash_lang_prototype):
    @wash_lang_prototype.command()
    @click.argument('script_file_path',
                    type=click.Path(), required=True, nargs=1)
    @click.option('--web_driver_path', help='Path to WebDriver executable.', required=True, type=str)
    @click.option('--browser_type', help='Browser type.', required=True,
                  type=click.Choice(['chrome', 'firefox', 'edge', 'opera'], case_sensitive=False),
                  default='chrome')
    @click.pass_context
    def execute(context, script_file_path, web_driver_path, browser_type):
        debug = context.obj['debug']
        try:
            options = WashOptions()
            if browser_type.casefold() == 'chrome':
                options.chrome_webdriver_path = web_driver_path
            if browser_type.casefold() == 'firefox':
                options.firefox_webdriver_path = web_driver_path
            if browser_type.casefold() == 'edge':
                options.edge_webdriver_path = web_driver_path
            if browser_type.casefold() == 'opera':
                options.opera_webdriver_path = web_driver_path

            execution_result = execute_wash_script(script_file_path=script_file_path, wash_options=options, debug=debug)
            print(execution_result)
        except Exception as e:
            raise click.ClickException(str(e))

        click.echo(f"WASH Script executed successfully. ({os.path.abspath(script_file_path)})")


def execute_wash_script(script_file_path, wash_options, debug=False) -> str:
    wash_script = Wash.from_file(script_file_path=script_file_path, options=wash_options, debug=debug)

    return wash_script.execute_as_json()
