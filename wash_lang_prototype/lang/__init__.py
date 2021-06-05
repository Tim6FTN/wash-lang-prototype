import os

from textx import language, metamodel_from_file


@language(name='wash', pattern='*.wash')
def wash_language():
    """
    WASH DSL - Web automation script helper domain specific language.
    """
    from .wash import wash_classes

    path_to_metamodel = os.path.join(os.path.dirname(__file__), 'wash.tx')
    meta_model = metamodel_from_file(path_to_metamodel, classes=wash_classes)
    return meta_model