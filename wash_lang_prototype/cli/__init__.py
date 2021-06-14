import pkg_resources

try:
    import click
except ImportError:
    raise Exception('Missing CLI dependencies. To use WASH from CLI, please run following command:/n'
                    'pip install wash-lang-prototype[cli]')


@click.group()
@click.option('--debug', default=False, is_flag=True, help="Debug/trace output.")
@click.pass_context
def wash_lang_prototype(context, debug):
    context.obj = {'debug': debug}


def register_wash_lang_prototype_subcommands():
    """
    Find and use all WASH sub-commands registered through the extension point.

    Entry point used for command registration is `wash_commands`.
    In this entry point you should register a callable that accepts the top level 
    click `wash_lang_prototype` command and register additional command(s) on it.
    """
    global wash_lang_prototype
    for subcommand in pkg_resources.iter_entry_points(group='wash_commands'):
        subcommand.load()(wash_lang_prototype)


# Register sub-commands specified through extension points.
register_wash_lang_prototype_subcommands()
