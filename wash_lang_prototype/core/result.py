import json


class ExecutionResult:
    """
    Base class for execution results.
    """
    def __init__(self, parent=None, **kwargs):
        self.__parent = parent
        self.add_attributes(**kwargs)

    def __repr__(self):
        return str(self.__get_dict())

    def __get_dict(self):
        """
        Returns the attribute dictionary of the object with omitted private attributes.
        """
        attributes_dictionary = self.__dict__.copy()
        attributes_dictionary.pop('_ExecutionResult__parent')

        return attributes_dictionary

    def add_attributes(self, **kwargs):
        """
        Adds given attributes to the instance.
        In case the instance already has a given attribute, it will update the existing attribute value
        by either adding new items to it, or replace the present values.
        """
        for attr_key, attr_value in kwargs.items():
            if not hasattr(self, attr_key):
                setattr(self, attr_key, attr_value)
            else:
                attribute = getattr(self, attr_key)
                if isinstance(attribute, ExecutionResult):
                    new_attributes = {k: attr_value.__dict__[k] for k
                                      in attr_value.__dict__ if k != '_ExecutionResult__parent'}
                    attribute.add_attributes(**new_attributes)
                elif isinstance(attribute, list):
                    # TODO (fivkovic): Handle case when len not equal
                    for new_item, existing_item in zip(attr_value, attribute):
                        new_attributes = {k: new_item.__dict__[k] for k
                                          in new_item.__dict__ if k != '_ExecutionResult__parent'}
                        existing_item.add_attributes(**new_attributes)
                else:
                    attribute = attr_value

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__get_dict())
