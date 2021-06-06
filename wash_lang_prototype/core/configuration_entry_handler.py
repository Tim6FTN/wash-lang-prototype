from typing import Any

from wash_lang_prototype.core.exceptions import WashError
from wash_lang_prototype.lang.wash import ConfigurationEntry, Configuration


def __extract_configuration_entry(configuration: Configuration, entry_name: str) -> ConfigurationEntry:
    """
    Extracts configuration entry from Configuration instance.
    In case the entry with given name is not found, a WashError is raised.
    Args:
        configuration(Configuration): Configuration instance to extract the entry from.
        entry_name(str): Name of the configuration entry.
    """
    configuration_entry = next(entry for entry in configuration.configuration_entries
                               if entry.type.name == entry_name)
    if not configuration_entry:
        raise WashError(f'Unable to find configuration entry "{entry_name}" in given configuration instance.')

    return configuration_entry


def __extract_parameter_value(configuration_entry: ConfigurationEntry, parameter_name: str) -> Any:
    """
    Extracts the parameter value from ConfigurationEntry instance.
    In case the parameter with given name is not found, a WashError is raised.
    Args:
        configuration_entry(ConfigurationEntry): ConfigurationEntry instance to extract the parameter value from.
        parameter_name(str): Name of the parameter in the entry.
    """
    parameter_value = next(parameter.value.value for parameter in configuration_entry.parameters
                           if parameter.parameter.name == parameter_name)
    if parameter_value is None:
        raise WashError(f'Parameter {parameter_name} does not exist in configuration entry '
                        f'"{configuration_entry.type.name}".')

    return parameter_value


def get_browser_type(configuration: Configuration) -> str:
    """
    Extracts 'browser type' configuration value from given configuration.
    Args:
        configuration(Configuration): Configuration instance to extract the value from.
    """
    entry = __extract_configuration_entry(configuration, 'browser_type')
    value = __extract_parameter_value(entry, 'browser_type')
    return value


def get_user_agent(configuration: Configuration) -> str:
    """
    Extracts 'user agent' configuration value from given configuration.
    Args:
        configuration(Configuration): Configuration instance to extract the value from.
    """
    entry = __extract_configuration_entry(configuration, 'user_agent')
    value = __extract_parameter_value(entry, 'user_agent')
    return value


def get_access_as_mobile_device(configuration: Configuration) -> bool:
    """
    Extracts 'access as mobile device' configuration value from given configuration.
    Args:
        configuration(Configuration): Configuration instance to extract the value from.
    """
    entry = __extract_configuration_entry(configuration, 'access_as_mobile_device')
    value = __extract_parameter_value(entry, 'is_active')
    return value


def get_use_incognito_mode(configuration: Configuration) -> bool:
    """
    Extracts 'use incognito mode' configuration value from given configuration.
    Args:
        configuration(Configuration): Configuration instance to extract the value from.
    """
    entry = __extract_configuration_entry(configuration, 'use_incognito_mode')
    value = __extract_parameter_value(entry, 'is_active')
    return value


def get_window_size(configuration: Configuration) -> tuple[int, int]:
    """
    Extracts 'window size' configuration value from given configuration.
    Args:
        configuration(Configuration): Configuration instance to extract the value from.
    """
    entry = __extract_configuration_entry(configuration, 'window_size')
    width_value = __extract_parameter_value(entry, 'width')
    height_value = __extract_parameter_value(entry, 'height')
    return width_value, height_value


def get_wait_timeout(configuration: Configuration) -> int:
    """
    Extracts 'wait timeout' configuration value from given configuration.
    Args:
        configuration(Configuration): Configuration instance to extract the value from.
    """
    entry = __extract_configuration_entry(configuration, 'wait_timeout')
    value = __extract_parameter_value(entry, 'timeout')
    return value