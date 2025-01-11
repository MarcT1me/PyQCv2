""" Main engine Window
"""
from pygame.display import set_mode, get_window_size, quit
from pygame import Rect
# Engine
import Engine
from Engine.graphic.window.win_data import WinData
from Engine.data import config
from Engine.math import vec2


class Window:
    def __init__(self, win_data: WinData):
        """ init main window """
        kwargs = {
            'size':  win_data.size,
            'flags': win_data.flags,
            'vsync': win_data.vsync,
        }
        if win_data.monitor not in (None, Engine.EMPTY) and str(win_data.monitor) not in 'nullEmptyType':
            kwargs['display'] = win_data.monitor
        self.__pg_win__ = set_mode(**kwargs)
    
    def __repr__(self):
        return f'<IWindow: t=\'{config.Win.title}\' s={get_window_size()}>'

    def fill(self, color, *, rect=None, special_flags=0):
        self.__pg_win__.fill(
            color,
            rect if rect is not None else Rect(0, 0, *self.__pg_win__.get_size()),
            special_flags
        )

    def blit(self, source, dest, *, area=None, special_flags=0):
        self.__pg_win__.blit(
            source,
            dest,
            area if area is not None else Rect(0, 0, *source.get_size()),
            special_flags
        )

    def get_size(self):
        return vec2(self.__pg_win__.get_size())

    @staticmethod
    def __quit__():
        quit()
