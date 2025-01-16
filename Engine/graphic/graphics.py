""" Engine Graphic core
"""
from loguru import logger
from typing import Optional
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
from Engine.mgl import create_context
from Engine.constants import EMPTY
from Engine.data.config import Win
from Engine.math import vec4, vec2


class Graphics:
    win_data: 'Engine.graphic.WinData' = EMPTY  # Window configs
    window: 'Engine.graphic.Window' = EMPTY  # Window
    gl_data: 'Optional[Engine.graphic.GlData]' = EMPTY
    context: 'Optional[Engine.mgl.Context]' = EMPTY  # MGL context

    interface: 'Optional[Engine.graphic.HardInterface]' = EMPTY  # Interface renderer

    """ other private """
    __monitors__ = get_monitors()

    def __new__(cls):
        cls.set_core()
        if cls.win_data.flags & OPENGL:
            cls.set_modern_gl()

    @classmethod
    def set_core(cls):
        """ set main variables"""
        cls.window = Engine.graphic.Window(win_data=cls.win_data)
        cls.set_caption(cls.win_data.title)
        cls.toggle_full(cls.win_data.is_desktop)

    @classmethod
    def resset(cls) -> None:
        cls.__release__()
        cls()
        if cls.win_data.flags & OPENGL:
            cls.set_modern_gl_configs()
        logger.debug(f'win.data = {cls.win_data}')

    @classmethod
    def set_modern_gl_configs(cls):
        cls.context.enable(flags=cls.gl_data.flags)
        cls.context.blend_func = cls.gl_data.blend_func
        cls.set_viewport(vec4(*cls.gl_data.view_start, *cls.win_data.size))
        # create interface surface
        cls.interface = cls.gl_data.interface_class()

    @classmethod
    def set_modern_gl(cls):
        """ set opengl attribute """
        display.gl_set_attribute(GL_CONTEXT_MAJOR_VERSION, cls.gl_data.minor_version)
        display.gl_set_attribute(GL_CONTEXT_MINOR_VERSION, cls.gl_data.minor_version)
        display.gl_set_attribute(GL_CONTEXT_PROFILE_MASK, cls.gl_data.profile_mask)
        logger.debug(f'set gl attributes, {cls.gl_data.minor_version, cls.gl_data.minor_version}')
        """ set all mgl """
        cls.context = create_context()

        cls.set_modern_gl_configs()

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

    @staticmethod
    def set_icon(_img):
        display.set_icon(_img)

    @staticmethod
    def set_caption(_caption):
        display.set_caption(_caption)

    @classmethod
    def toggle_full(cls, is_desktop: bool = False):
        """ toggle fullscreen """
        if cls.win_data.full:
            if cls.win_data.full:
                # find window into any monitor
                index, monitor = cls.get_current_monitor()
                # calculate flags and sizes
                size = vec2(monitor.width, monitor.height)
                flags = Win.flags | FULLSCREEN
            else:
                index = EMPTY
                size = Win.size
                flags = Win.flags
            # setting changes
            cls.win_data = cls.win_data.extern(
                {
                    'size': size,
                    'monitor': index,
                }
            )

            if is_desktop:
                cls.win_data.extern({'flags': flags})
                cls.resset()
            else:
                display.toggle_fullscreen()

    @staticmethod
    def is_full():
        return display.is_fullscreen()

    @staticmethod
    def get_current_size() -> vec2:
        return vec2(display.get_window_size())

    @classmethod
    def get_current_monitor(cls):
        # iter on all monitors and find current window display
        win = getWindowsWithTitle(cls.win_data.title)[0]
        for index, monitor in enumerate(cls.__monitors__):
            if monitor.x <= win.left and monitor.y <= win.top or \
                    monitor.x <= win.left + win.width and monitor.y <= win.top or \
                    monitor.x <= win.left and monitor.y <= win.top + win.height or \
                    monitor.x <= win.left + win.width and monitor.y <= win.top + win.height:
                return index, monitor
        else:
            return None, None

    @staticmethod
    def get_monitor_sizes() -> list[vec2]:
        return list(map(vec2, display.get_desktop_sizes()))

    @classmethod
    def get_current_monitor_size(cls) -> vec2:
        index, monitor = cls.get_current_monitor()
        return vec2(monitor.width, monitor.height)

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
    def __release__(cls) -> None:
        if cls.win_data is not EMPTY and cls.win_data.flags & OPENGL:
            try:
                cls.interface.__destroy__()
                cls.context.release()
            except Exception as exc:
                logger.error(f'can`t release context, {exc.args[0]}')
        if cls.window is not EMPTY:
            del cls.window
