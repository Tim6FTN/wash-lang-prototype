try:
    import click
except ImportError:
    raise Exception('Missing CLI dependencies')


def version(wash_lang_prototype):
    @wash_lang_prototype.command()
    def version():
        import wash_lang_prototype
        click.echo('wash_lang_prototype {}'.format(wash_lang_prototype.__version__))