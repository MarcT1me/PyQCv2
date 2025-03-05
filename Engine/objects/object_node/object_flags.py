from enum import Flag, auto


class ObjectStatusFlags(Flag):
    Active = auto()

    Renderable = auto()
    Visible = auto()

    Static = auto()
    Dynamic = auto()

    @property
    def is_active(self) -> bool:
        return self & self.Active

    @property
    def is_renderable(self) -> bool:
        return self & self.Renderable

    @property
    def is_visible(self) -> bool:
        return self & self.Visible

    @property
    def is_static(self) -> bool:
        return self & self.Static

    @property
    def is_dynamic(self) -> bool:
        return self & self.Dynamic
