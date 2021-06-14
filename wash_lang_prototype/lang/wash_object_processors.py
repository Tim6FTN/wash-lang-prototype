from wash_lang_prototype.core.exceptions import WashLanguageError


def configuration_object_processor(configuration):
    """
    Validates if all Configuration names are unique in the WASH script.
    """
    configuration_names = [configuration.name for configuration in configuration.parent.configuration_definitions]
    for configuration_name in configuration_names:
        if configuration_names.count(configuration_name) > 1:
            raise WashLanguageError(f'Configuration with the name {configuration_name} already exists. '
                                    f'Names of configurations in a WASH script must be unique.')


def configuration_entry_object_processor(configuration_entry):
    """
    Validates:
        1. If values for all required parameters are specified in a single configuration entry.
        2. If values for all required parameters are unique in a single configuration entry.
        3. If all values in a single configuration entry are defined as values in the relevant ConfigurationOption.
    """
    parameters_in_configuration_entry = [p.parameter for p in configuration_entry.parameters]

    for parameter in configuration_entry.type.parameters:
        if parameter.required and parameter not in parameters_in_configuration_entry:
            raise WashLanguageError(f'A required parameter "{parameter.name}" is missing from '
                                    f'{configuration_entry.type.name} configuration option '
                                    f'in the configuration "{configuration_entry.parent.name}"')

    for parameter_entry in parameters_in_configuration_entry:
        if parameter_entry not in configuration_entry.type.parameters:
            raise WashLanguageError(f'Unknown/Unsupported parameter "{parameter_entry.name}" of configuration option '
                                    f'{configuration_entry.type.name} has been defined '
                                    f'in the configuration "{configuration_entry.parent.name}"')
        if parameters_in_configuration_entry.count(parameter_entry) > 1:
            raise WashLanguageError(f'Parameter "{parameter_entry.name}" of configuration option '
                                    f'{configuration_entry.type.name} has been defined '
                                    f'multiple times in the configuration "{configuration_entry.parent.name}"')


def configuration_parameter_value_object_processor(configuration_parameter_value):
    """
    Validates if all configuration parameter value types match the defined parameter type.
    """

    type_map = {
        "string[]": list,
        "integer[]": list,
        "float[]": list,
        "boolean[]": list,
        "string": str,
        "integer": int,
        "float": float,
        "boolean": bool
    }

    sub_type_map = {
        "string[]": str,
        "integer[]": int,
        "float[]": float,
        "boolean[]": bool
    }

    parameter_type = configuration_parameter_value.parameter.parameter_type
    parameter_value = configuration_parameter_value.value.value

    if not isinstance(parameter_value, type_map.get(parameter_type)):
        raise WashLanguageError(f'The type of the parameter "{configuration_parameter_value.parameter.name}" '
                                f'of configuration option {configuration_parameter_value.parent.type.name} '
                                f'must be {parameter_type}.')
    elif isinstance(parameter_value, list) and not all(isinstance(x.value, sub_type_map.get(parameter_type))
                                                       for x in parameter_value):
        raise WashLanguageError(f'The type of a value in the parameter "{configuration_parameter_value.parameter.name}"'
                                f' of configuration option {configuration_parameter_value.parent.type.name} '
                                f'must be {parameter_type}.')
