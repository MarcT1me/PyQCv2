""" Various additional structures for data storage
"""
from typing import Self, Any

import Engine


class AttributesKeeper(dict):
    """ Hybrid attribute-dictionary container with default values
    """

    def __init__(self, default: Any = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default = default

    def __getattr__(self, name):
        if name in self:
            return self[name]
        return self.__dict__.get(name, self._default)

    def __setattr__(self, key, value):
        if key in self.__dict__:  # Служебные атрибуты
            self.__dict__[key] = value
        elif key in self:  # Существующие ключи словаря
            self[key] = value
        else:  # Новые атрибуты
            self.__dict__[key] = value

    def __getitem__(self, key):
        return super().get(key, self._default)

    def __contains__(self, key):
        return super().__contains__(key) or key in self.__dict__


class Roster(AttributesKeeper):
    """ A container for storing objects in a tree structure,
    inherited from AttributesKeeper
    """

    def __init__(self, name: str = "root", branch_type: Engine.CLS = None, *args, **kwargs):
        self.name = name
        self._branch_type = Roster if branch_type is None else branch_type
        super().__init__(*args, **kwargs)

    def new_branch(self, name: str, *args, **kwargs) -> Self:
        self[name] = self._branch_type(name, default=self._default, *args, **kwargs)
        return self

    def use(self, method_name: str, calling_filter: Engine.FUNC, *args, **kwargs) -> None:
        for i in tuple(self.values()):
            if not calling_filter(i):
                getattr(i, method_name)(*args, **kwargs)
