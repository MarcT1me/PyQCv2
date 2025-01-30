""" Main engine Window
"""
from pygame.display import set_mode, get_window_size, quit

import Engine
from Engine.graphic.window.win_data import WinData
from Engine.data import config
from Engine.math import vec2


class Window:
    def __init__(self, win_data: WinData):
        """ init main window """
        kwargs = {
            'size': win_data.size,
            'flags': win_data.flags,
            'vsync': win_data.vsync,
        }
        if win_data.monitor not in (None, Engine.EMPTY) and str(win_data.monitor) not in 'nullEmptyType':
            kwargs['display'] = win_data.monitor
        self.__pg_win__ = set_mode(**kwargs)

    def __repr__(self):
        return f'<IWindow: t=\'{config.Win.name}\' s={get_window_size()}>'

    def blit(self, *args, **kwargs):
        self.__pg_win__.blit(*args, **kwargs)

    def get_size(self):
        return vec2(self.__pg_win__.get_size())

    @staticmethod
    def __quit__():
        quit()
