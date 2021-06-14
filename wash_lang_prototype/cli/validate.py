import codecs
import os

from textx import metamodel_for_language


try:
    import click
except ImportError:
    raise Exception('Missing CLI dependencies. To use WASH from CLI, please run following command:/n'
                    'pip install wash-lang-prototype[cli]')


def validate(wash_lang_prototype):
    @wash_lang_prototype.command()
    @click.argument('wash_file', type=click.Path(), required=True)
    @click.pass_context
    def validate(context, wash_file):
        from wash_lang_prototype.core.exceptions import WashError, WashLanguageError

        debug = context.obj['debug']
        try:
            script_file_path = os.path.abspath(wash_file)
            with codecs.open(script_file_path, 'r') as script_file:
                script = script_file.read()

                metamodel = metamodel_for_language('wash')
                _ = metamodel.model_from_str(script, file_name=wash_file, debug=debug)

            click.echo(f"WASH Script is validated successfully. ({os.path.abspath(wash_file)})")
        except WashError as wex:
            raise click.ClickException(str(wex))
        except Exception as ex:
            message = ex.message if hasattr(ex, 'message') else str(ex)
            raise click.ClickException(str(WashLanguageError(message)))
