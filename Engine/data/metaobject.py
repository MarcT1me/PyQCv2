import Engine


class MetaObjectError(Exception): pass


class MetaObjectDataDelegationError(MetaObjectError): pass


class MetaObject:
    data: 'Engine.data.MetaData | Engine.data.TimedMetaData'
    # MetaData
    id: 'Engine.data.Identifier'

    def __init__(self, data: 'Engine.data.MetaData'):
        self.__dict__["_data"]  = data

    @property
    def data(self):
        return self.data

    def __getattr__(self, name):
        if hasattr(self._data, name):
            try:
                return getattr(self._data, name)
            except Exception as e:
                raise MetaObjectDataDelegationError(f"Cant delegate field {name} from self.data") from e
        raise AttributeError(f"'{self.__class__.__name__}' not have a attr '{name}'")

    def __setattr__(self, name, value):
        if hasattr(self._data, name):
            try:
                setattr(self._data, name, value)
            except Exception as e:
                raise MetaObjectDataDelegationError(f"Cant delegate field {name} from self.data") from e
        else:
            super().__setattr__(name, value)

    def __delattr__(self, name):
        if hasattr(self._data, name):
            try:
                delattr(self._data, name)
            except Exception as e:
                raise MetaObjectDataDelegationError(f"Cant delegate field {name} from self.data") from e
        else:
            super().__delattr__(name)
