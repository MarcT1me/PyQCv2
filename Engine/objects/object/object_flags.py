from enum import Flag, auto


class ObjectFlags(Flag):
    Active = auto()

    Renderable = auto()
    Visible = auto()
