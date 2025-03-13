from typing_extensions import Self, deprecated
from array import array

from loguru import logger

import Engine
from Engine.graphic.interface.interface import Interface


@deprecated("marked to remove, low-impact interface class")
class HardInterface(Interface):
    swizzle = "RGBA"
    filter = (Engine.mgl.NEAREST, Engine.mgl.NEAREST)
    anisotropy = 32.0

    def __init__(self) -> None:
        self.surface = Engine.pg.Surface(
            Engine.App.graphic.__gl_system__.gl_data.interface_resolution, flags=Engine.pg.SRCALPHA
        )

        self.shader: Engine.graphic.GL.Shader = Engine.App.assets.storage.Shader.definite("interface").content
        # self.shader = Engine.App.assets.get("Engine::interface_shader").content

        self.texture: Engine.mgl.Texture = Engine.App.graphic.__gl_system__.context.texture(
            Engine.App.graphic.__gl_system__.gl_data.interface_resolution, len(self.swizzle)
        )
        self.texture.filter, self.texture.swizzle = (Engine.mgl.NEAREST, Engine.mgl.NEAREST), self.swizzle
        self.texture.build_mipmaps()
        self.texture.anisotropy = self.anisotropy

        self.__vbo = Engine.App.graphic.__gl_system__.context.buffer(data=array('f', [
            # position (x, y), uv cords (x, y)
            -1.0, -1.0, 0.0, 1.0,  # bottom left
            1.0, -1.0, 1.0, 1.0,  # bottom right
            -1.0, 1.0, 0.0, 0.0,  # top left
            1.0, 1.0, 1.0, 0.0,  # top right
        ]))
        self.__vao = Engine.App.graphic.__gl_system__.context.vertex_array(
            self.shader.program, [(self.__vbo, '2f 2f', 'vertices', 'texCoord')], skip_errors=True
        )

    def __str__(self):
        return (f"HardInterface<>(size: {Engine.math.vec2(self.surface.get_size())} "
                f"format: {self.swizzle} "
                f"anisotropy {self.anisotropy})")

    def __enter__(self) -> Self:
        Engine.App.graphic.interface.surface.fill((0, 0, 0, 0))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> False:
        self.__render__()
        return False

    @staticmethod
    def _write_data_(surf, tex, *, _s='RGBA') -> Engine.mgl.Texture:
        image_data = Engine.pg.image.tostring(surf, _s)
        tex.write(image_data)
        return tex

    def __render__(self) -> None:
        self._write_data_(self.surface, self.texture).use(0)
        self.shader['interfaceTexture'] = 0

        self.__vao.render(mode=Engine.mgl.TRIANGLE_STRIP)

    def release(self):
        self.destroy()
        self.shader.release()
        self.__vbo.release()
        self.__vao.release()
        logger.info("Interface released")

    def destroy(self) -> None:
        self.texture.release()
