from wash_lang_prototype.core.exceptions import WashError


def configuration_options_object_processor(configuration_options):
    """
    Validates if all ConfigurationOption names are unique in the ConfigurationOptions instance.
    """
    option_names = [option.name for option in configuration_options.configuration_options]
    for option_name in option_names:
        if option_names.count(option_name) > 1:
            raise WashError(f'Configuration option with the name {option_name} already exists. '
                            f'Names of configuration options in a WASH internal script must be unique.')


def configuration_option_object_processor(configuration_option):
    """
    Validates if all ConfigurationOptionParameter names are unique in the ConfigurationOption instance.
    Also validates if at least one required parameter is specified in the ConfigurationOption instance.
    """
    parameter_names = [parameter.name for parameter in configuration_option.parameters]
    for parameter_name in parameter_names:
        if parameter_names.count(parameter_name) > 1:
            raise WashError(f'Parameter with the name {parameter_name} already exists '
                            f'in the configuration option {configuration_option.name}. '
                            f'Names of parameters in a configuration option type must be unique.')

    if all(not parameter.required for parameter in configuration_option.parameters):
        raise WashError(f'No required parameters are specified '
                        f'in the configuration option {configuration_option.name}. '
                        f'Each configuration option requires at least 1 required parameter.')
