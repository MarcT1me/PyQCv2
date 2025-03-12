from loguru import logger
from pprint import pformat

import Engine

from Engine.objects.ireleasable import IReleasable


class GlSystem(IReleasable):
    def __init__(self, win_data: 'Engine.graphic.WinData'):
        self.gl_data: Engine.graphic.GL.GlData = None
        self.update_gl_data(win_data)
        self.context: Engine.mgl.Context = None  # MGL context

        # change window data flags - switch to OPENGL
        win_data.flags |= Engine.pg.OPENGL

        # set OpenGL args
        Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_MAJOR_VERSION, self.gl_data.minor_version)
        Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_MINOR_VERSION, self.gl_data.minor_version)
        Engine.pg.display.gl_set_attribute(Engine.pg.GL_CONTEXT_PROFILE_MASK, self.gl_data.profile_mask)

        logger.info(
            f'Engine GlSystem - init\n'
            f'gl attrs: {self.gl_data.minor_version, self.gl_data.minor_version}\n'
            f'gl data:\n'
            f'{pformat(self.gl_data)}\n'
        )

    def update_gl_data(self, win_data):
        self.gl_data = Engine.App.instance.__gl_data__(win_data)

    def init_context(self):
        self.context = Engine.mgl.create_context()

        self._set_gl_configs()

        logger.info(
            "Engine GLSystem - init context\n"
            f"context info:\n"
            f"{pformat(self.context.info)}\n"
        )

    def _set_gl_configs(self) -> None:
        self.context.enable(flags=self.gl_data.flags)
        self.context.blend_func = self.gl_data.blend_func
        self.update_viewport()

    def update_viewport(self) -> None:
        self.context.viewport = self.gl_data.view

    def clear(self):
        self.context.clear(color=self.gl_data.clear_color)

    def release(self):
        self.context.release()
