import os

from textx import language, metamodel_from_file


@language(name='wash', pattern='*.wash')
def wash_language():
    """
    WASH DSL - Web automation script helper domain specific language.
    """

    meta_model = metamodel_from_file(os.path.join(os.path.dirname(__file__), 'wash.tx'), autokwd=True)

    return meta_model