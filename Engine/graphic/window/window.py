""" Main engine Window
"""
from pygetwindow import Window as _Win
from loguru import logger
from pprint import pformat
from screeninfo import get_monitors

import Engine
from Engine.graphic.window.win_data import WinData
from Engine.data import config
from Engine.math import vec2


class Window:
    init_without_size: bool = True

    __monitors__ = get_monitors()

    for monitor in __monitors__:
        if monitor.is_primary:
            __monitors__.remove(monitor)
            __monitors__.insert(0, monitor)

    def __init__(self, win_data: WinData):
        self.data: WinData = win_data

        self.windowed_size: Engine.math.ivec2 = self.data.size
        self.fullscreen_size: Engine.math.ivec2 = self.data.size

        self.windowed_pos: Engine.math.ivec2 = Engine.math.ivec2(0, 0)

        # create window
        self.set_mode(without_size=Window.init_without_size and win_data.full and win_data.frameless)

        """ init main window """
        self.utils: _Win = None
        self.__pg_win__ = None

        logger.info(
            "Engine graphic Window - init\n"
            f"data:\n"
            f"{pformat(self.data)}\n"
        )

    def swap_sizes(self):
        if self.data.full:
            self.windowed_size = self.data.size
            self.data.size = self.fullscreen_size
        else:
            self.fullscreen_size = self.data.size
            self.data.size = self.windowed_size

    def set_mode(self, *, without_size=False):
        kwargs = self.data.to_kwargs()
        if without_size: kwargs.pop("size")
        logger.info(
            f"Engine Window - set_mode\n"
            f"size: {self.data.size}\n"
            f"kwargs: {kwargs}"
        )
        self.__pg_win__ = Engine.pg.display.set_mode(**kwargs)

    def toggle_full(self) -> None:
        """ toggle fullscreen """
        index, monitor_size = self.get_current_monitor()

        if self.data.frameless:
            self.fullscreen_size = Engine.math.ivec2(monitor_size)
            if self.data.full:
                self.data.flags = self.data.flags | Engine.pg.NOFRAME
            else:
                self.data.flags = self.data.flags & ~Engine.pg.NOFRAME
        else:
            self.data.flags = \
                self.data.flags | Engine.pg.FULLSCREEN if self.data.full else \
                    self.data.flags & ~Engine.pg.FULLSCREEN

        # resset window
        self.swap_sizes()
        self.data.monitor = index

        logger.info(
            f"Engine Window - toggle_full\n"
            f"full: {self.data.full}\n"
            f"size:\t{self.data.size}\n"
            f"monitor:\t{self.data.monitor}\n"
            f"flags:\t{self.data.flags}\n"
        )

    @staticmethod
    def set_icon(_img: Engine.pg.Surface) -> None:
        Engine.pg.display.set_icon(_img)

    @staticmethod
    def set_caption(_caption: str) -> None:
        Engine.pg.display.set_caption(_caption)

    @staticmethod
    def is_full() -> bool:
        return Engine.pg.display.is_fullscreen()

    @staticmethod
    def get_window_size() -> Engine.math.vec2:
        return Engine.math.vec2(Engine.pg.display.get_window_size())

    def get_current_monitor(self) -> tuple[int, tuple[int, int]]:
        return self.data.monitor, Engine.pg.display.get_desktop_sizes()[self.data.monitor]

    def __post_init__(self):
        from pygetwindow import getWindowsWithTitle
        self.data.flags = self.data.flags | Engine.pg.SHOWN
        self.toggle_full()
        self.set_caption(self.data.title)
        self.set_icon(
            Engine.pg.image.load(
                f"{Engine.data.FileSystem.APPLICATION_ICO_dir}\\{Engine.data.FileSystem.APPLICATION_ICO_name}"
            )
            # Engine.App.assets.get(self.data.ico_path).content
        )
        self.set_mode()
        self.utils = getWindowsWithTitle(self.data.title)[0]

    def __repr__(self):
        return f'<Window: {config.WinDefault.title} ({Engine.pg.display.get_window_size()})>'

    def blit(self, *args, **kwargs):
        self.__pg_win__.blit(*args, **kwargs)

    def get_surf_size(self):
        return vec2(self.__pg_win__.get_size())

    @staticmethod
    def __quit__():
        Engine.pg.display.quit()
