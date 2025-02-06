""" Engine Graphic core
"""
from loguru import logger
from typing import Optional, final
# window utils
from screeninfo import get_monitors, Monitor

import Engine


@final
class System:
    def __init__(self):
        self.__monitors = get_monitors()

        # window
        self.win_data: Engine.graphic.WinData = None  # Window configs
        self.window: Engine.graphic.Window = None  # Window

        # gl
        self.gl_data: Optional[Engine.graphic.GlData] = None
        self.context: Optional[Engine.mgl.Context] = None  # MGL context
        # game ui surface
        self.interface: Optional[Engine.graphic.HardInterface] = None  # Interface renderer

        self._set_data()  # set data from App methods

        # set start attributes
        if self.gl_data:
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_MAJOR_VERSION, self.gl_data.minor_version)
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_MINOR_VERSION, self.gl_data.minor_version)
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_PROFILE_MASK, self.gl_data.profile_mask)
            logger.debug(f'set gl attributes, {self.gl_data.minor_version, self.gl_data.minor_version}')

        # init sub-systems
        self._init_window()
        self._init_gl()

    def _set_data(self):
        self.win_data: Engine.graphic.WinData = Engine.app.App.InheritedСlass.__win_data__()  # Window configs
        self.gl_data: Optional[Engine.graphic.GlData] = Engine.app.App.InheritedСlass.__gl_data__(self.win_data)

    def _init_window(self) -> None:
        """ set main variables"""
        self.win_data.flags = self.win_data.flags | Engine.pg.HIDDEN
        self.window = Engine.graphic.Window(win_data=self.win_data)

        self.set_caption(self.win_data.name)
        self.set_icon(
            Engine.pg.image.load(
                f"{Engine.data.File.APPLICATION_path}\\{Engine.data.File.APPLICATION_ICO_dir}"
                f"\\{Engine.data.File.APPLICATION_ICO_name}"
            )
        )
        self.toggle_full()

    def _init_gl(self) -> None:
        """ set opengl attribute """
        self.context = Engine.mgl.create_context()

        self._set_gl_configs()

        logger.info(
            f"\n\tEngine graphic - init\n"
            f"screen:\n"
            f"\tWinData = {self.win_data};\n"
            f"context:\n"
            f"\tsize = {self.context.screen.size} \tGPU = {self.context.info['GL_RENDERER']};\n"
        )

    def _set_gl_configs(self) -> None:
        self.context.enable(flags=self.gl_data.flags)
        self.context.blend_func = self.gl_data.blend_func
        self.set_viewport(self.gl_data.view)

    def __post__init__(self):
        self.win_data.flags = self.win_data.flags | Engine.pg.SHOWN
        self.window.set_mode(self.win_data)
        self.window.set_utils()
        self.interface = self.gl_data.interface_type()

    def resset(self) -> None:
        self.interface.__destroy__()
        self._set_data()  # set data from App methods
        self.__post__init__()
        self._set_gl_configs()

    def set_viewport(self, viewport: Engine.math.vec4) -> None:
        self.context.viewport = viewport

    def toggle_full(self) -> None:
        """ toggle fullscreen """
        if self.win_data.full:
            # find window into any monitor
            index, monitor = self.get_current_monitor()
            # calculate flags and sizes
            size = Engine.math.vec2(monitor.width, monitor.height)
            flags = Engine.data.Win.flags | Engine.pg.FULLSCREEN
        else:
            index = None
            size = Engine.data.Win.size
            flags = Engine.data.Win.flags
        # setting changes
        self.win_data = self.win_data.extern(
            {
                'size': size,
                'monitor': index,
            }
        )

        if self.win_data.is_desktop:
            self.win_data.extern({'flags': flags})
            self.resset()
        else:
            Engine.pg.display.toggle_fullscreen()

    def get_current_monitor(self) -> tuple[int, Monitor]:
        # iter on all monitors and find current window display
        win = self.window.utils
        for index, monitor in enumerate(self.__monitors):
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
