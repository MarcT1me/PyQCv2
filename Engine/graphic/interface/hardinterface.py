from array import array
from loguru import logger
# import moderngl
import Engine


class HardInterface:
    _s = "RGBA"
    _f = (Engine.mgl.NEAREST, Engine.mgl.NEAREST)
    _a = 32.0

    def __init__(self) -> None:
        self.surface = Engine.pg.Surface(Engine.graphic.Graphics.win_data.size, flags=Engine.pg.SRCALPHA)

        self.shader = Engine.graphic.GL.Shader(
            f"{Engine.data.File.__ENGINE_DATA__}\\{Engine.data.File.SHADER_dir}\\"
            f"interface",
            Engine.VERTEX_SHADER | Engine.FRAGMENT_SHADER,
            Engine.TEXT
        )

        self.texture: Engine.mgl.Texture = Engine.graphic.Graphics.context.texture(self.surface.get_size(), 4)
        self.texture.filter, self.texture.swizzle = self._f, self._s
        self.texture.build_mipmaps()
        self.texture.anisotropy = self._a

        self.__vbo = Engine.graphic.Graphics.context.buffer(data=array('f', [
            # position (x, y), uv cords (x, y)
            -1.0, -1.0, 0.0, 1.0,  # bottom left
            1.0, -1.0, 1.0, 1.0,  # bottom right
            -1.0, 1.0, 0.0, 0.0,  # top left
            1.0, 1.0, 1.0, 0.0,  # top right
        ]))
        self.__vao = Engine.graphic.Graphics.context.vertex_array(
            self.shader.program, [(self.__vbo, '2f 2f', 'vertices', 'texCoord')], skip_errors=True
        )
        logger.success('Interface - init\n')

    def __enter__(self):
        Engine.graphic.Graphics.interface.surface.fill((0, 0, 0, 0))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Engine.graphic.Graphics.interface.__render__()
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

    def __destroy__(self) -> None:
        self.texture.release()
        self.shader.__release__()
        self.__vbo.release()
        self.__vao.release()
