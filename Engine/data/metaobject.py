import Engine


class MetaObject:
    data: 'Engine.data.MetaData | Engine.data.TimedMetaData'
    # MetaData
    id: str
    name: str

    def __init__(self, data: 'Engine.data.MetaData'):
        self.data = data
        self.data.link_to_object(self)