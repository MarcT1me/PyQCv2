""" Engine Graphic core
"""
from typing import Optional, final
from pprint import pformat

from loguru import logger

import Engine
from Engine.graphic.interface.interface import Interface
from Engine.graphic.GL.shader.shader_roster import ShadersRoster


@final
class System:
    def __init__(self, gl_attribute_data: 'Optional[Engine.graphic.GL.GlAttributesData]' = None):
        # window
        win_data: Engine.graphic.WinData = Engine.App.instance.__win_data__()
        self.window: Engine.graphic.Window = None  # Window

        # gl
        self.gl_data: Optional[Engine.graphic.GL.GlData] = None
        self.context: Optional[Engine.mgl.Context] = None  # MGL context
        # game ui surface
        self.interface: Optional[Interface] = None  # Interface renderer

        # set start attributes
        if Engine.data.MainData.IS_USE_GL:
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_MAJOR_VERSION, gl_attribute_data.minor_version)
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_MINOR_VERSION, gl_attribute_data.minor_version)
            Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_PROFILE_MASK, gl_attribute_data.profile_mask)
            logger.info(f'set gl attributes, {gl_attribute_data.minor_version, gl_attribute_data.minor_version}\n')

            """ rosters and sub-systems """
            self.shader_roster = ShadersRoster()

        # init sub-systems
        self._init_window(win_data)

        logger.success("Engine graphic System - init\n")

    def __post_init__(self):
        logger.info("Engine graphic System - __post__init__")

        self.window.__post_init__()

        if Engine.data.MainData.IS_USE_GL:
            self._init_gl()
            self._init_interface()
        else:
            self.interface = Engine.graphic.SdlInterface()

    def _init_window(self, win_data: 'Engine.graphic.WinData') -> None:
        """ set main variables"""
        win_data.flags = win_data.flags | Engine.pg.HIDDEN
        self.window = Engine.graphic.Window(win_data)

    def _init_gl(self) -> None:
        """ set opengl attribute """
        self.gl_data = Engine.App.instance.__gl_data__(self.window.data)

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
        self.interface = self.gl_data.interface_type()
        logger.success(f"Interface initialized: {self.interface}")

    def resset(self) -> None:
        self.window.set_mode()

        if Engine.data.MainData.IS_USE_GL:
            self.gl_data = Engine.App.__gl_data__(self.window.data)  # set data from App methods

            self._init_interface()

            self.set_viewport(self.gl_data.view)
        else:
            self.interface = Engine.graphic.SdlInterface()

        logger.success("Engine graphic System - resset\n")

    def set_viewport(self, viewport: Engine.math.vec4) -> None:
        self.context.viewport = viewport

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
            with Engine.failures.Catch(identifier="Graphic system GL release", is_critical=False,
                                       is_handling=False) as cth:
                cth.try_func(self.interface.release)
                cth.try_func(self.context.release)
        if self.window is not None:
            del self.window
