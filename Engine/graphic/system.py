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
        win_data: Engine.graphic.WinData = Engine.App.inherited.__win_data__()
        self.window: Engine.graphic.Window = None  # Window

        # gl
        self.gl_data: Optional[Engine.graphic.GL.GlData] = Engine.App.inherited.__gl_data__(win_data)
        self.context: Optional[Engine.mgl.Context] = None  # MGL context
        # game ui surface
        self.interface: Optional[Engine.graphic.HardInterface] = None  # Interface renderer

        # set start attributes
        if self.gl_data:
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_MAJOR_VERSION, self.gl_data.minor_version)
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_MINOR_VERSION, self.gl_data.minor_version)
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_PROFILE_MASK, self.gl_data.profile_mask)
            logger.info(f'set gl attributes, {self.gl_data.minor_version, self.gl_data.minor_version}\n')

        """ rosters and sub-systems """
        self.shader_roster = Engine.graphic.GL.ShadersRoster()

        # init sub-systems
        self._init_window(win_data)
        self._init_gl() if self.gl_data else Ellipsis

        logger.success("Engine graphic System - init\n")

    def _init_window(self, win_data: 'Engine.graphic.WinData') -> None:
        """ set main variables"""
        win_data.flags = win_data.flags | Engine.pg.HIDDEN
        self.window = Engine.graphic.Window(win_data)

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
        self.set_caption(self.window.data.title)
        self.set_icon(
            Engine.pg.image.load(
                f"{Engine.data.FileSystem.APPLICATION_ICO_dir}"
                f"\\{Engine.data.FileSystem.APPLICATION_ICO_name}"
            )
        )
        self.window.data.flags = self.window.data.flags | Engine.pg.SHOWN
        self.window.__post_init__()
        self.toggle_full()

        """ Load default Shaders """
        self.shader: Engine.graphic.GL.Shader = Engine.App.assets.load(
            Engine.assets.AssetFileData(
                id=Engine.data.Identifier("interface"),  # interface shader
                type=Engine.DataType.Shader,
                dependencies=[
                    Engine.assets.AssetFileData(
                        type=(Engine.DataType.Text | Engine.DataType.Shader, Engine.ShaderType.Vertex),
                        path=f"{Engine.data.FileSystem.APPLICATION_path}\\{Engine.data.FileSystem.ENGINE_SHADER_dir}\\"
                             f"interface.vert"
                    ),
                    Engine.assets.AssetFileData(
                        type=(Engine.DataType.Text | Engine.DataType.Shader, Engine.ShaderType.Fragment),
                        path=f"{Engine.data.FileSystem.APPLICATION_path}\\{Engine.data.FileSystem.ENGINE_SHADER_dir}\\"
                             f"interface.frag"
                    ),
                ]
            )
        )

        self.interface = self.gl_data.interface_type()

    def resset(self) -> None:
        self.window.set_mode(self.window.data)

        if self.gl_data:
            self.gl_data = Engine.App.__gl_data__(self.window.data)  # set data from App methods

            self.interface.__destroy__()
            self.interface = self.gl_data.interface_type()

            self._set_gl_configs()

        logger.success("Engine graphic System - resset\n")

    def set_viewport(self, viewport: Engine.math.vec4) -> None:
        self.context.viewport = viewport

    def toggle_full(self) -> None:
        """ toggle fullscreen """
        index, monitor = self.get_current_monitor()
        monitor_size = Engine.math.vec2(monitor.width, monitor.height)

        if self.window.data.full:
            # find window into any monitor
            # calculate flags and sizes
            size = monitor_size
            flags = self.window.data | Engine.pg.FULLSCREEN

            if self.window.data.is_desktop:
                self.window.data.modify({'flags': flags})
                self.resset()
            else:
                Engine.pg.display.toggle_fullscreen()
        else:
            index = None
            size = Engine.data.WinDefault.size if self.window.data.size == monitor_size else self.window.data.size
            if self.window.data.flags & Engine.pg.FULLSCREEN:
                flags = self.window.data.flags | ~Engine.pg.FULLSCREEN
            else:
                flags = self.window.data.flags
        # setting changes
        self.window.data = self.window.data.modify(
            {
                'size': size,
                'monitor': index,
            }
        )

        logger.info(
            f"Engine graphic System - toggle_full{' (desktop)' if self.window.data.is_desktop else ''}\n"
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
                self.interface.__release__()
                self.context.release()
            except Exception as exc:
                logger.error(f'can`t release GL, {exc.args[0]}')
        if self.window is not None:
            del self.window
