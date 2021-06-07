from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Handler(ABC):
    """
    Represents an interface that declares a method for building a chain of handlers,
    otherwise known as the chain of responsibility pattern.
    It also declares a method for executing a request using the chain of handlers.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        """
        Sets the next handler in the chain.
        Args:
            handler(Handler): The next handler in the chain.
        """
        pass

    @abstractmethod
    def handle(self, request: Any) -> Any:
        """
        Handles the given request by executing the chain of registered handlers.
        All concrete Handlers either handle the request or pass it to the next handler in the chain.
        Args:
            request: The request to be handled by the chain.
        """
        pass


class ObjectFactory(ABC):
    """
    Represents a general purpose Object Factory that can be used to create all kinds of objects.
    Provides a method to register a Builder based on a key value
    and a method to create the concrete object instances based on the key.
    """
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs) -> Any:
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)
