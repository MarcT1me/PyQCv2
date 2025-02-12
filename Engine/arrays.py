""" Various additional structures for data storage
"""
from argparse import ArgumentError
from typing import Self, Any

import Engine


class AttributesKeeperError(Exception):
    pass


class AttributesKeeper(dict):
    """ Hybrid attribute-dictionary container with default values
    """

    def __init__(self, default: Any = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default = default

    def __getattr__(self, name):
        try:
            if name in self:
                return self[name]
            return self.__dict__.get(name, self._default)
        except Exception as e:
            raise AttributesKeeperError(f"Cant get attribute {name}")

    def __setattr__(self, key, value):
        try:
            if key in self.__dict__:  # Служебные атрибуты
                self.__dict__[key] = value
            elif key in self:  # Существующие ключи словаря
                self[key] = value
            else:  # Новые атрибуты
                self.__dict__[key] = value
        except Exception as e:
            raise AttributesKeeperError(f"Cant set attribute {key}")

    def __getitem__(self, key):
        return super().get(key, self._default)

    def __contains__(self, key):
        return super().__contains__(key) or key in self.__dict__


class RosterError(Exception):
    pass


class Roster(AttributesKeeper):
    """ A container for storing objects in a tree structure,
    inherited from AttributesKeeper
    """

    def __init__(self, name: str = "root", *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

    def new_branch(self, name: str, *args, **kwargs) -> Self:
        if name in self:
            raise RosterError(f"Branch with name {name} already in roster")

        try:
            self.__setattr__(name, self.__class__(name, default=self._default, *args, **kwargs))
        except Exception as e:
            raise RosterError(f"Cant create branch with name {name} - {e.__class__.__name__}") from e
        finally:
            return self

    def use(self, method_name: str, calling_filter: Engine.FUNC, *args, **kwargs) -> None:
        for i in tuple(self.values()):
            if not calling_filter(i):
                try:
                    getattr(i, method_name)(*args, **kwargs)
                except AttributeError as e:
                    raise RosterError(
                        f"Cant use method {method_name} for {i.__class__.__name__} - method not exist") from e
                except ArgumentError as e:
                    raise RosterError(
                        f"Cant use method {method_name} for {i.__class__.__name__} - mistake in arguments") from e

    def branch(self, name: str) -> Self | None:
        """ Return (Roster type) branch or None if not exist """
        return getattr(self, name, None)
