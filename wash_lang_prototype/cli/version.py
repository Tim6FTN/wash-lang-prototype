try:
    import click
except ImportError:
    raise Exception('Missing CLI dependencies. To use WASH from CLI, please run following command:/n'
                    'pip install wash-lang-prototype[cli]')


def version(wash_lang_prototype):
    @wash_lang_prototype.command()
    def version():
        """
        Displays the WASH package version.
        """
        import wash_lang_prototype
        click.echo('wash_lang_prototype {}'.format(wash_lang_prototype.__version__))
