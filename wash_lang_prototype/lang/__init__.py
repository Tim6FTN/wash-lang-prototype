import os

from textx import language, metamodel_from_file, scoping, metamodel_for_language


@language(name='wash', pattern='*.wash')
def wash_language():
    """
    WASH DSL - Web automation script helper domain specific language.
    """
    from .wash import wash_classes
    from .wash_object_processors import configuration_object_processor, configuration_entry_object_processor,\
        configuration_parameter_value_object_processor

    wash_internal_meta_model = metamodel_for_language('wash_internal')
    internal_folder = os.path.join(os.path.dirname(__file__), '..', 'internal')

    # NOTE: Refer to https://github.com/textX/textX/blob/master/textx/scoping/__init__.py#L35-L290
    builtin_models_repository = scoping.ModelRepository()

    for internal_file in os.listdir(internal_folder):
        internal_file_model = wash_internal_meta_model.model_from_file(os.path.join(internal_folder, internal_file))
        builtin_models_repository.add_model(internal_file_model)

    object_processors_map = {
        'Configuration': configuration_object_processor,
        'ConfigurationEntry': configuration_entry_object_processor,
        'ConfigurationParameterValue': configuration_parameter_value_object_processor
    }

    path_to_metamodel = os.path.join(os.path.dirname(__file__), 'wash.tx')
    meta_model = metamodel_from_file(path_to_metamodel,
                                     classes=wash_classes,
                                     builtin_models=builtin_models_repository, 
                                     autokwd=True,
                                     auto_init_attributes=False)

    meta_model.register_obj_processors(object_processors_map)
    meta_model.register_scope_providers({
        "*.*": scoping.providers.PlainNameImportURI(),
        "ConfigurationParameterValue.parameter": scoping.providers.RelativeName(
            "parent.type.parameters"),
    })

    return meta_model


@language(name='wash_internal', pattern='*.washy')
def wash_internal_language(**kwargs):
    """
    WASH Internal DSL - domain specific language used internally to extend WASH.
    """
    from .wash_internal import internal_classes
    from .wash_internal_object_processors import configuration_options_object_processor, \
        configuration_option_object_processor

    object_processors_map = {
        'ConfigurationOptions': configuration_options_object_processor,
        'ConfigurationOption': configuration_option_object_processor
    }

    path_to_metamodel = os.path.join(os.path.dirname(__file__), 'wash_internal.tx')
    meta_model = metamodel_from_file(path_to_metamodel, classes=internal_classes, autokwd=True, **kwargs)

    internal_folder = os.path.join(os.path.dirname(__file__), '..', 'internal')
    model = meta_model.model_from_file(os.path.join(internal_folder, 'configuration_options.washy'))

    meta_model.register_obj_processors(object_processors_map)

    return meta_model
