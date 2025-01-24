from typing import Callable, Any
import Engine


class AttributesKeeper:
    """ A class that should store attributes and replace the dictionary """

    def __new__(cls, default=Engine.EMPTY):
        instance = super().__new__(cls)
        instance._default = default
        return instance

    def __getitem__(self, item):
        if hasattr(self, item):
            exec(f'self.last = self.{item}')
        else:
            self.last = self._default
        return self.last

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getattr__(self, item):
        setattr(self, item, self._default)
        return self._default


class Roster(dict):
    def new_branch(self, name: str):
        setattr(self, name, Roster())
        return self

    def use(self, method_name: str, *args, calling_filter: Callable[[Any], bool], **kwargs):
        for i in tuple(self.values()):
            if not calling_filter(i):
                getattr(i, method_name)(*args, **kwargs)

    def release(self):
        for i in self.values():
            i.release()
        self.clear()
