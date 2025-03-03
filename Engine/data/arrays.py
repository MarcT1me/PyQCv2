""" Various additional structures for data storage
"""
from typing import Self, Any, final
from argparse import ArgumentError

import Engine


@final
class DataTable:
    def __init__(self, **data):
        self._data = data

    def get(self, item: 'str | Engine.data.Identifier'):
        return self._data.get(str(item), None)

    def __getattr__(self, item):
        return self.get(item)


class AttributesKeeperError(Exception): pass


class AttributesKeeper(dict):
    """ Hybrid attribute-dictionary container with default values
    """

    def __init__(self, default: Any = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default = default

    def __getattr__(self, name) -> Self | Any:
        try:
            if name in self:
                return self[name]
            return self.__dict__.get(name, self._default)
        except Exception as e:
            raise AttributesKeeperError(f"Cant get attribute {name}") from e

    def __setattr__(self, key, value) -> None:
        try:
            if key in self.__dict__:  # Служебные атрибуты
                self.__dict__[key] = value
            elif key in self:  # Существующие ключи словаря
                self[key] = value
            else:  # Новые атрибуты
                self.__dict__[key] = value
        except Exception as e:
            raise AttributesKeeperError(f"Cant set attribute {key}") from e

    def __getitem__(self, key) -> Any:
        return super().get(key, self._default)

    def __contains__(self, key) -> bool:
        return super().__contains__(key) or key in self.__dict__


class RosterError(Exception): pass


class SimpleRoster(AttributesKeeper):
    """ A container for storing objects in a categorises,
    inherited from dict
    """

    def __new__(cls, *args, **kwargs):
        __obj: Self = super().__new__(cls)
        __annotations = cls.__dict__.get("__annotations__", {})
        for __attr, __annotation_type in __annotations.items():
            __default_value: Any = cls.__dict__.get(__attr)
            __obj.new_branch(__attr, value=__default_value if __default_value else __annotation_type())
        return __obj

    def __init__(self, name: str = "root", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = Engine.data.Identifier(name=name)
        self._branch_ids: set[str] = {}

    @property
    def branches(self) -> list[dict]:
        return [self.branch(identifier) for identifier in self._branch_ids]

    def new_branch(self, name: str, value: Any = dict()) -> Self:
        """ create dict as attribute in roster with name """
        if name in self:
            raise RosterError(f"Branch with name {name} already in roster")

        try:
            self[name] = value
            self._branch_ids.add(name)
        except Exception as e:
            raise RosterError(f"Cant create branch with name {name} - {e.__class__.__name__}") from e
        finally:
            return self

    def use(self, method_name: str, calling_filter: Engine.FUNC, *args, **kwargs) -> None:
        """ use method with the method_name on all object_node in current roster """

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

    def branch(self, name: str) -> dict | None:
        """ Return branch dict or None if not exist """
        return self.get(name, None)


class Roster(SimpleRoster):
    """ A container for storing objects in a tree structure,
    inherited from SimpleRoster and change new_branch method (create new Roster)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.branch_ids: set[Engine.data.Identifier] = {}

    def new_branch(self, name: str, *args, **kwargs) -> Self:
        """ create embedded Roster as attribute in current roster with name """
        if name in self:
            raise RosterError(f"Branch with name {name} already in roster")

        try:
            branch = self.__class__(name, default=self._default, *args, **kwargs)
            self.__setattr__(name, branch)
            self.branch_ids.add(branch.id)
        except Exception as e:
            raise RosterError(f"Cant create branch with name {name} - {e.__class__.__name__}") from e
        finally:
            return self

    def branch(self, name: str) -> Self | None:
        """ Return (Roster type) branch or None if not exist """
        return getattr(self, name, None)
