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

    @classmethod
    def update(cls, changes: dict) -> None:
        for key, value in changes.items():
            exec(f'cls.{key} = value')
