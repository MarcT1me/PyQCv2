from pygame.surface import Surface
from pygame.rect import Rect
from pygame.constants import FULLSCREEN, RESIZABLE, NOFRAME
import pygame._sdl2.video as sdl2_video


import Engine
from Engine.graphic.window.node_win_data import NodeWinData
from Engine.data.config import Win
from Engine.math import vec2


class NodeWindow:
    roster = dict()

    def __init__(self, win_data: NodeWinData, *, modal_window=None):
        """ init confirm window class """
        assert win_data.id not in NodeWindow.roster, "NodeWindow<_Id: str> arg already in roster"
        self.id = win_data.id
        self.win_data = win_data

        self.surf: Surface = Surface(size=win_data.size)  # create window surface
        self.rect = Rect(0, 0, *win_data.size)
        """ setting window """
        self.win: sdl2_video.Window = sdl2_video.Window(
            title=win_data.name
        )
        self.win.set_modal_for(Engine.app.App.graphic.window._pg_win if not modal_window else modal_window)
        self.update()

        """ other window and render variables """
        self._renderer: sdl2_video.Renderer = sdl2_video.Renderer(self.win)  # create window texture from surface
        self._rend_tex: sdl2_video.Texture = sdl2_video.Texture.from_surface(self._renderer, self.surf)

        NodeWindow.roster[win_data.id] = self

    def update(self):
        if self.win_data.monitor is not None:
            monitor = Engine.app.App.graphic.__monitors[self.win_data.monitor]
            self.pos = vec2(monitor.x, -monitor.y)
        if self.win_data.pos is not None:
            self.pos += self.win_data.pos
        self.size = self.win_data.size
        self.opacity = self.win_data.opacity
        self.relative_mouse = self.win_data.relative_mouse
        self.set_resizable(self.win_data.flags & RESIZABLE)
        self.set_borderless(self.win_data.flags & NOFRAME)
        self.set_fullscreen(self.win_data.flags & FULLSCREEN)
        """ renderer """
        # viewport
        self._renderer.set_viewport(
            (0, 0, *self.win_data.size)
        )

    def set_fullscreen(self, is_full, desktop=True) -> None:
        self.win.set_fullscreen(desktop) if is_full else self.win.set_windowed()

    def set_borderless(self, is_borderless):
        self.win.borderless = is_borderless

    def set_resizable(self, is_resizable):
        self.win.resizable = is_resizable

    @property
    def relative_mouse(self) -> bool:
        return self.win.relative_mouse

    @relative_mouse.setter
    def relative_mouse(self, value: bool) -> None:
        self.win.relative_mouse = value

    @property
    def opacity(self) -> int:
        return self.win.opacity

    @opacity.setter
    def opacity(self, value: int) -> None:
        self.win.opacity = value

    @property
    def size(self) -> vec2:
        return self.win.size

    @size.setter
    def size(self, value: vec2) -> None:
        self.rect = Rect(0, 0, *self.win_data.size)
        self.win.size = value

    @property
    def pos(self) -> vec2:
        return vec2(self.win.position)

    @pos.setter
    def pos(self, value: vec2) -> None:
        self.win.position = value

    def set_visibility(self, visibility: bool) -> None:
        self.win.show() if visibility else self.win.hide()

    def get_surf(self) -> Surface:
        return self._renderer.to_surface()

    def get_rect(self) -> Rect:
        return self._rend_tex.get_rect()

    def flip(self) -> None:
        self.__update_tex__()
        self.__render__()

    def __update_tex__(self) -> None:
        self._rend_tex.update(self.surf)

    def __render__(self) -> None:
        self._renderer.clear()
        self._renderer.blit(
            self._rend_tex, self.rect, self.rect
        )
        self._renderer.present()

    def release(self) -> None:
        self.win.destroy()
        NodeWindow.roster.pop(self.id)


def roster_render() -> None:
    for win in NodeWindow.roster.values():
        win.flip()


def roster_relies() -> None:
    for win in list(NodeWindow.roster.values()):
        win.release()
