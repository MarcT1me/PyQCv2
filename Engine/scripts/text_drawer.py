from typing import Any
from dataclasses import dataclass, field

import Engine


@dataclass
class TextField:
    font: Engine.pg.font.Font
    text: str
    format_args: list[Any]

    alias: bool
    color: Any
    bg_color: Any = None

    _rnd: Engine.pg.Surface = field(init=False)
    _inited: bool = True

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self._update_rnd() if "_inited" in self.__dict__ and key != "_rnd" else Ellipsis

    def _update_rnd(self):
        self._rnd = self.font.render(self.text.format(*self.format_args), self.alias, self.color, self.bg_color)

    @property
    def rnd(self):
        if not self._rnd:
            self._update_rnd()
        return self._rnd


class TextDrawer:
    def __init__(
            self, pos: Engine.math.vec2,
            text: list[list[TextField]] = []
    ):
        self.text: list[list[TextField]] = text

        self.pos = pos

    def render(self, surf):
        dy = 0
        for line in self.text:
            line_dy = 0
            dx = 0
            for textfield in line:
                self.draw_field(surf, textfield, dx, dy)
                dx += textfield.rnd.get_width()
                line_dy = max(line_dy, textfield.rnd.get_height())
            dy = line_dy

    def draw_field(self, surf, textfield: TextField, dx: int, dy: int):
        surf.blit(textfield.rnd, self.pos + Engine.math.vec2(dx, dy))
