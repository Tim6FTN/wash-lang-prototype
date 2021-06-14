from abc import ABC


class WashInternalBase(ABC):
    """
    Represents the base class for all custom classes used during the internal meta-model instantiation.
    """
    def __init__(self, *args, **kwargs):
        if args:
            self.parent = args[0]
        for key, item in kwargs.items():
            setattr(self, key, item)
        super().__init__()


class ConfigurationOptions(WashInternalBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConfigurationOption(WashInternalBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConfigurationOptionParameter(WashInternalBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


internal_classes = [
    ConfigurationOptions,
    ConfigurationOption,
    ConfigurationOptionParameter
]
