""" Main engine Window
"""
from pygetwindow import Window as _Win
from loguru import logger
from pprint import pformat

import Engine
from Engine.graphic.window.win_data import WinData
from Engine.data import config
from Engine.math import vec2


class Window:
    def __init__(self, win_data: WinData):
        self.data: WinData = None
        self.set_mode(win_data)
        """ init main window """
        self.utils: _Win = None
        self.__pg_win__ = None

        logger.info(
            "Engine graphic Window - init\n"
            f"data:\n"
            f"{pformat(self.data)}\n"
        )

    def set_mode(self, win_data: WinData):
        self.data = win_data
        kwargs = self.data.to_kwargs()
        logger.info(
            f"Engine Window - set_mode\n"
            f"kwargs: {kwargs}"
        )
        self.__pg_win__ = Engine.pg.display.set_mode(**kwargs)

    def __post_init__(self):
        self.set_mode(self.data)
        from pygetwindow import getWindowsWithTitle
        self.utils = getWindowsWithTitle(self.data.name)[0]

    def __repr__(self):
        return f'<Window: {config.WinDefault.name} ({Engine.pg.display.get_window_size()})>'

    def blit(self, *args, **kwargs):
        self.__pg_win__.blit(*args, **kwargs)

    def get_size(self):
        return vec2(self.__pg_win__.get_size())

    @staticmethod
    def __quit__():
        Engine.pg.display.quit()
