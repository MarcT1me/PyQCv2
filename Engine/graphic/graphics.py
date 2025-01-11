""" Engine Graphic core
"""
from loguru import logger
from typing import TYPE_CHECKING
# window utils
from pygetwindow import getWindowsWithTitle
from screeninfo import get_monitors

import Engine.graphic
# for Graphics
from Engine.pg import (
    FULLSCREEN, OPENGL,
    GL_CONTEXT_MAJOR_VERSION, GL_CONTEXT_MINOR_VERSION,
    GL_CONTEXT_PROFILE_MASK,
    display, event, mouse, cursors, Surface
)
from Engine.mgl import Context, create_context
from Engine.constants import EMPTY
from Engine.objects.camera import Camera
from Engine.data.config import Win
from Engine.math import vec4

if TYPE_CHECKING:
    from Engine.graphic import WinData, Window, GlData, HardInterface


class Graphics:
    win_data: 'WinData' = EMPTY  # Window configs
    gl_data: 'GlData' = EMPTY
    window: 'Window' = EMPTY  # Window
    context: Context = EMPTY  # MGL context

    interface: 'HardInterface' = EMPTY  # Interface renderer

    """ other private """
    __monitors__ = get_monitors()

    @classmethod
    def set_core(cls):
        """ set main variables"""
        cls.window = Engine.graphic.Window(win_data=cls.win_data)
        display.set_caption(cls.win_data.title)
        cls.toggle_full(Win.full)
        cls.camera = Camera()
        cls.flip()

    @classmethod
    def set_modern_gl(cls):
        """ set opengl attribute """
        display.gl_set_attribute(GL_CONTEXT_MAJOR_VERSION, cls.gl_data.minor_version)
        display.gl_set_attribute(GL_CONTEXT_MINOR_VERSION, cls.gl_data.minor_version)
        display.gl_set_attribute(GL_CONTEXT_PROFILE_MASK, cls.gl_data.profile_mask)
        logger.debug(f'set gl attributes, {cls.gl_data.minor_version, cls.gl_data.minor_version}')
        """ set all mgl """
        cls.context = create_context()

        cls.context.enable(flags=cls.gl_data.flags)
        cls.context.blend_func = cls.gl_data.blend_func
        cls.set_viewport(vec4(*cls.gl_data.view, *cls.win_data.size))
        # create interface surface
        cls.interface = cls.gl_data.interface_class()

        logger.info(
            f"\n\tEngine graphic - init\n"
            f"screen:\n"
            f"\tWinData = {cls.win_data};\n"
            f"context:\n"
            f"\tsize = {cls.context.screen.size} \tGPU = {cls.context.info['GL_RENDERER']};\n"
        )

    @classmethod
    def set_viewport(cls, viewport: vec4):
        cls.context.viewport = viewport

    @classmethod
    def get_display_index(cls):
        # find window
        win = getWindowsWithTitle(cls.win_data.title)[0]
        # iter on all monitors and find current window display
        for index, monitor in enumerate(cls.__monitors__):
            if monitor.x <= win.left and monitor.y <= win.top or \
                    monitor.x <= win.left + win.width and monitor.y <= win.top or \
                    monitor.x <= win.left and monitor.y <= win.top + win.height or \
                    monitor.x <= win.left + win.width and monitor.y <= win.top + win.height:
                return index, monitor
        else:
            return None, None

    @staticmethod
    def set_icon(_img):
        display.set_icon(_img)

    @staticmethod
    def set_caption(_caption):
        display.set_caption(_caption)

    @classmethod
    def toggle_full(cls, _is_full):
        """ toggle fullscreen """
        if _is_full != cls.is_full():
            # find window into any monitor
            index, monitor = cls.get_display_index()
            # calculate flags and sizes
            if not cls.is_full():
                width = monitor.width
                height = monitor.height
                flags = Win.flags | FULLSCREEN
            else:
                width = Win.size[0]
                height = Win.size[1]
                index = EMPTY  # if not full change monitor on NONE
                flags = Win.flags

            # setting changes
            cls.win_data = cls.win_data.extern(
                {
                    'width': width,
                    'height': height,
                    'monitor': index,
                    'flags': flags
                }
            )

            cls.resset()

    @classmethod
    def set_desktop_full(cls, _is_full):
        """ Set full screen YES/NO  """
        if _is_full != cls.is_full():
            # calculate flags and sizes
            if not cls.is_full():
                flags = Win.flags | FULLSCREEN
            else:
                flags = Win.flags
            # setting changes
            cls.win_data = cls.win_data.extern(
                {
                    'flags': flags
                }
            )
            cls.resset()
            display.toggle_fullscreen()

    @staticmethod
    def is_full():
        return display.is_fullscreen()

    @staticmethod
    def set_cursor_mode(visible: bool = None, grab: bool = None) -> None:
        mouse.set_visible(visible if visible is not None else mouse.get_visible())
        event.set_grab(grab if grab is not None else event.get_grab())

    @staticmethod
    def set_cursor_image(image: Surface, hotspot: tuple = (0, 0)) -> None:
        cursor = cursors.Cursor(hotspot, image)
        mouse.set_cursor(cursor)

    @staticmethod
    def set_cursor_style(system: int) -> None:
        mouse.set_cursor(system)

    @staticmethod
    def flip():
        display.flip()

    @classmethod
    def resset(cls):
        cls.window = Engine.graphic.Window(win_data=cls.win_data)
        if cls.win_data.flags & OPENGL:
            cls.set_viewport(vec4(*cls.gl_data.view, *cls.win_data.size))
            cls.interface = cls.gl_data.interface_class()
        logger.debug(f'win.data = {cls.win_data}')

    @classmethod
    def __release__(cls):
        if cls.win_data and cls.win_data.flags & OPENGL:
            try:
                cls.interface.__destroy__()
                cls.context.release()
            except Exception as exc:
                logger.error(f'can`t release context, {exc.args[0]}')
        if cls.window:
            cls.window.__quit__()


def event_window(_event: event.Event):
    return getattr(_event, 'window', None)


def get_desktop_sizes() -> list[tuple[int, int]]:
    return display.get_desktop_sizes()


def get_current_desktop_size() -> tuple[int, int]:
    index, _ = Graphics.get_display_index()
    return get_desktop_sizes()[index]


def get_window_size() -> tuple[int, int]:
    return display.get_window_size()
