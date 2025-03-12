""" Engine Graphic core
"""
from typing import Optional, final

from loguru import logger

import Engine
from Engine.graphic.interface.interface import Interface

from Engine.objects.iinitanle import IPostInitable
from Engine.objects.ireleasable import IReleasable


@final
class GraphicSystem(IPostInitable, IReleasable):
    def __init__(self):
        # window
        self.window: Engine.graphic.Window = None  # Window
        self.interface: Optional[Interface] = None  # Interface renderer

        win_data: Engine.graphic.WinData = Engine.App.instance.__win_data__()

        self.__gl_system__: Optional[Engine.graphic.GL.GlSystem] = None

        # init sub-systems
        if Engine.data.MainData.IS_USE_GL:
            self.__gl_system__ = Engine.graphic.GL.GlSystem(win_data)
        self._init_window(win_data)

        logger.success("Engine graphic System - init\n")

    def __post_init__(self):
        logger.info("Engine graphic System - __post__init__")

        self.window.__post_init__()

        if Engine.data.MainData.IS_USE_GL:
            self.__gl_system__.init_context()
            self.prepare = lambda: self.__gl_system__.clear()
        else:
            self.prepare = lambda: self.window.__pg_win__.fill("black")
            self._init_interface = lambda: setattr(self, "interface", Engine.graphic.SdlInterface())

        self._init_interface()

    def _init_window(self, win_data: 'Engine.graphic.WinData') -> None:
        """ set main variables"""
        win_data.flags = win_data.flags | Engine.pg.HIDDEN
        self.window = Engine.graphic.Window(win_data)

    def _init_interface(self):
        if not Engine.App.assets.storage.has_asset("interface"):
            Engine.App.assets.load(
                Engine.assets.AssetFileData(
                    id=Engine.data.Identifier("interface"),  # interface shader
                    type=Engine.DataType.Shader,
                    dependencies=[
                        Engine.assets.AssetFileData(
                            type=(Engine.DataType.Text | Engine.DataType.Shader, Engine.ShaderType.Vertex),
                            path=f"{Engine.data.FileSystem.ENGINE_DATA_path}\\"
                                 f"{Engine.data.FileSystem.PRESETS_dir}\\shaders\\"
                                 f"interface.vert"
                        ),
                        Engine.assets.AssetFileData(
                            type=(Engine.DataType.Text | Engine.DataType.Shader, Engine.ShaderType.Fragment),
                            path=f"{Engine.data.FileSystem.ENGINE_DATA_path}\\"
                                 f"{Engine.data.FileSystem.PRESETS_dir}\\shaders\\"
                                 f"interface.frag"
                        ),
                    ]
                )
            )
        if self.interface: self.interface.destroy()
        self.interface = self.__gl_system__.gl_data.interface_type()
        logger.success(f"Interface initialized: {self.interface}")

    def resset(self) -> None:
        self.window.set_mode()

        if Engine.data.MainData.IS_USE_GL:
            self.__gl_system__.update_gl_data(self.window.data)

            self._init_interface()

            self.__gl_system__.update_viewport()
        else:
            self._init_interface()

        logger.success("Engine graphic System - resset\n")

    def prepare(self):
        """ Prepare graphic system to rendering """
        ...

    @staticmethod
    def flip() -> None:
        Engine.pg.display.flip()

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

    def release(self) -> None:
        if self.__gl_system__:
            with Engine.failures.Catch(identifier="Graphic system GL release", is_critical=False,
                                       is_handling=False) as cth:
                cth.try_func(self.interface.release)
                cth.try_func(self.__gl_system__.release)
        if self.window is not None:
            del self.window
