""" Main engine Window
"""
from pygetwindow import Window as _Win

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
        self._pg_win = None

    def set_mode(self, win_data: WinData):
        self.data = win_data
        self._pg_win = Engine.pg.display.set_mode(**self.data.to_kwargs())

    def set_utils(self):
        from pygetwindow import getWindowsWithTitle
        self.utils = getWindowsWithTitle(self.data.name)[0]

    def __repr__(self):
        return f'<Window: {config.Win.name} ({Engine.pg.display.get_window_size()})>'

    def blit(self, *args, **kwargs):
        self._pg_win.blit(*args, **kwargs)

    def get_size(self):
        return vec2(self._pg_win.get_size())

    @staticmethod
    def __quit__():
        Engine.pg.display.quit()
