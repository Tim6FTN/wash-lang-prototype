

class ConfigurationOptions:
    def __init__(self, configuration_options):
        self.configuration_options = configuration_options


class ConfigurationOption:
    def __init__(self, parent, name, description, parameters):
        self.parent = parent
        self.name = name
        self.description = description
        self.parameters = parameters


class ConfigurationOptionParameter:
    def __init__(self, parent, required, parameter_type, name):
        self.parent = parent
        self.required = required
        self.parameter_type = parameter_type
        self.name = name


internal_classes = [
    ConfigurationOptions,
    ConfigurationOption,
    ConfigurationOptionParameter
]