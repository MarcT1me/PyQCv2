""" Engine Graphic core
"""
from loguru import logger
from typing import Optional, final
from pprint import pformat
# window utils
from screeninfo import get_monitors, Monitor

import Engine


@final
class System:
    def __init__(self):
        self.__monitors__ = get_monitors()

        # window
        win_data: Engine.graphic.WinData = Engine.app.App.InheritedСlass.__win_data__()
        self.window: Engine.graphic.Window = None  # Window

        # gl
        self.gl_data: Optional[Engine.graphic.GlData] = Engine.app.App.InheritedСlass.__gl_data__(win_data)
        self.context: Optional[Engine.mgl.Context] = None  # MGL context
        # game ui surface
        self.interface: Optional[Engine.graphic.HardInterface] = None  # Interface renderer

        # set start attributes
        if self.gl_data:
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_MAJOR_VERSION, self.gl_data.minor_version)
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_MINOR_VERSION, self.gl_data.minor_version)
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_PROFILE_MASK, self.gl_data.profile_mask)
            logger.info(f'set gl attributes, {self.gl_data.minor_version, self.gl_data.minor_version}\n')

        # init sub-systems
        self._init_window(win_data)
        self._init_gl() if self.gl_data else Ellipsis

        logger.success("Engine graphic System - init\n")

    def _init_window(self, win_data: 'Engine.graphic.WinData') -> None:
        """ set main variables"""
        win_data.flags = win_data.flags | Engine.pg.HIDDEN
        self.window = Engine.graphic.Window(win_data)

        self.set_caption(self.window.data.name)
        self.set_icon(
            Engine.pg.image.load(
                f"{Engine.data.FileSystem.APPLICATION_path}\\{Engine.data.FileSystem.APPLICATION_ICO_dir}"
                f"\\{Engine.data.FileSystem.APPLICATION_ICO_name}"
            )
        )
        self.toggle_full()

    def _init_gl(self) -> None:
        """ set opengl attribute """
        self.context = Engine.mgl.create_context()

        self._set_gl_configs()

        logger.info(
            "Engine graphic System - init (GL)\n"
            f"data:\n"
            f"{pformat(self.gl_data)}\n"
            f"context info:\n"
            f"{pformat(self.context.info)}\n"
        )

    def _set_gl_configs(self) -> None:
        self.context.enable(flags=self.gl_data.flags)
        self.context.blend_func = self.gl_data.blend_func
        self.set_viewport(self.gl_data.view)

    def __post_init__(self):
        self.window.data.flags = self.window.data.flags | Engine.pg.SHOWN
        self.window.set_mode(self.window.data)
        self.window.__post_init__()
        self.interface = self.gl_data.interface_type()

    def resset(self) -> None:
        self.window.set_mode(self.window.data)

        if self.gl_data:
            self.gl_data = Engine.app.App.InheritedСlass.__gl_data__(self.window.data)  # set data from App methods

            self.interface.__destroy__()
            self.interface = self.gl_data.interface_type()

            self._set_gl_configs()

        logger.success("Engine graphic System - resset")

    def set_viewport(self, viewport: Engine.math.vec4) -> None:
        self.context.viewport = viewport

    def toggle_full(self) -> None:
        """ toggle fullscreen """
        if self.window.data.full:
            # find window into any monitor
            index, monitor = self.get_current_monitor()
            # calculate flags and sizes
            size = Engine.math.vec2(monitor.width, monitor.height)
            flags = self.window.data | Engine.pg.FULLSCREEN
        else:
            index = None
            size = Engine.data.WinDefault.size
            flags = Engine.data.WinDefault.flags
        # setting changes
        self.window.data = self.window.data.extern(
            {
                'size': size,
                'monitor': index,
            }
        )

        if self.window.data.is_desktop:
            self.window.data.extern({'flags': flags})
            self.resset()
        else:
            Engine.pg.display.toggle_fullscreen()

        logger.info(
            f"Engine graphic System - toggle_full{' (desktop)' if self.window.data.is_desktop else ''}"
            f"full: {self.window.data.full}\n"
            f"size:\t{size}\n"
            f"monitor:\t{index}\n"
            f"flags:\t{flags}\n"
        )

    def get_current_monitor(self) -> tuple[int, Monitor]:
        # iter on all monitors and find current window display
        win = self.window.utils
        for index, monitor in enumerate(self.__monitors__):
            if monitor.x <= win.left and monitor.y <= win.top or \
                    monitor.x <= win.left + win.width and monitor.y <= win.top or \
                    monitor.x <= win.left and monitor.y <= win.top + win.height or \
                    monitor.x <= win.left + win.width and monitor.y <= win.top + win.height:
                return index, monitor
        else:
            return None, None

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
    def get_current_size() -> Engine.math.vec2:
        return Engine.math.vec2(Engine.pg.display.get_window_size())

    @staticmethod
    def get_monitor_sizes() -> tuple[Engine.math.vec2]:
        return list(map(Engine.math.vec2, Engine.pg.display.get_desktop_sizes()))

    @staticmethod
    def set_cursor_mode(visible: bool = None, grab: bool = None) -> None:
        Engine.pg.mouse.set_visible(visible if visible is not None else Engine.pg.mouse.get_visible())
        Engine.pg.event.set_grab(grab if grab is not None else Engine.pg.event.get_grab())

    @staticmethod
    def set_cursor_image(image: Engine.pg.Surface, hotspot: tuple = (0, 0)) -> None:
        cursor = Engine.pg.cursors.Cursor(hotspot, image)
        Engine.pg.mouse.set_cursor(cursor)

    @staticmethod
    def set_cursor_style(system: int) -> None:
        Engine.pg.mouse.set_cursor(system)

    @staticmethod
    def flip() -> None:
        Engine.pg.display.flip()

    def __release__(self) -> None:
        if self.gl_data:
            try:
                self.interface.__destroy__()
                self.context.release()
            except Exception as exc:
                logger.error(f'can`t release GL, {exc.args[0]}')
        if self.window is not None:
            del self.window
