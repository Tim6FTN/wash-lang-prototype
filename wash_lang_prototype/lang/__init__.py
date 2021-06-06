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



@language(name='wash_internal', pattern='*.washy')
def wash_internal_language(**kwargs):
    """
    WASH Internal DSL - domain specific language used internally to extend WASH.
    """
    from .wash_internal import internal_classes

    path_to_metamodel = os.path.join(os.path.dirname(__file__), 'wash_internal.tx')
    meta_model = metamodel_from_file(path_to_metamodel, classes=internal_classes, autokwd=True, **kwargs)

    internal_folder = os.path.join(os.path.dirname(__file__), '..', 'internal')
    model = meta_model.model_from_file(os.path.join(internal_folder, 'configuration_options.washy'))


    return meta_model