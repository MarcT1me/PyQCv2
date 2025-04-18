# graphics
import pygame
import moderngl

# other
import glob
from loguru import logger
from copy import copy


class Texture:
    """ Namelist your Texture`s.

    accounting Texture:
     * CustomTexture_name['some name'] = "texture_path.texture_ext"


    # custom Texture`s init.
    for name, path in Texture.name.items():
        self.textures[name] = self.get_texture(path)

    * !!! attention: init before Mash class !!!
    """

    name: dict[str: str] = dict()

    def __init__(self) -> None:
        """ NOT USE THIS INITIALIZATION;

          * !!! attention: add our textures before Mash class !!!

         """
        # textures array
        self.textures: dict[str: moderngl.Texture] = {
            'test1': self.__get_texture__(
                path=rf'{config.ENGINE_DATA_path}/{config.TEXTURE_path}/test_texture.jpg'
            ),
            'empty': self.__get_texture__(
                path=rf'{config.ENGINE_DATA_path}/{config.TEXTURE_path}/no_textures.jpg'
            ),
            'box1': self.__get_texture__(
                path=rf'{config.ENGINE_DATA_path}/{config.TEXTURE_path}/box1.jpg'
            ),
            'wall1': self.__get_texture__(
                path=rf'{config.ENGINE_DATA_path}/{config.TEXTURE_path}/wall1.jpg'
            ),
            # 'skybox': self.__get_texture_cube__(dir_path='textures/skybox1/', ext='png'),
            'depth_texture': self.__get_depth_texture__(),
        }

        # load custom texture
        for name, (form, atr, f_path, m_ext, t_ext) in CustomVBO_name.items():
            self.textures[name] = self.__get_texture__(self.__get_custom_texture_name__(path=f_path, ext=t_ext))

        for name, path in Texture.name.items():
            self.textures[name] = self.__get_texture__(path)

        logger.debug('Textures load - finished\n')

    def add(self, name, path) -> None:
        self.textures[name] = self.__get_texture__(path)

    @staticmethod
    def __get_custom_texture_name__(path, ext) -> str:
        """ get name texture custom model """
        logger.debug(rf'    search texture: {path}/*.{ext}')
        t_list = glob.glob(rf'{path}/*.{ext}')
        return t_list[0] if ext is not None \
            else rf'{config.ENGINE_DATA_path}/{config.TEXTURE_path}/no_textures.jpg'

    def __get_texture__(self, path) -> moderngl.Texture:
        """ load texture """
        try:
            texture = pygame.image.load(path).convert_alpha()
        except FileNotFoundError:
            texture = self.textures['empty']

        texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)  # debug
        # texture.fill((255, 0, 0))  # debug
        texture = self.ctx.texture(size=texture.get_size(), components=4,
                                   data=pygame.image.tostring(texture, 'RGBA'))  # get GLSL texture array
        # use GLSL methods
        texture.filter = moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        logger.info(rf'Texture with name: {path.split("/")[-1]} - load')

        return texture

    def __get_texture_cube__(self, dir_path, ext) -> moderngl.TextureCube:
        """ use that load SkyBox """

        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        textures = []
        for face in faces:
            texture = pygame.image.load(dir_path + f'{face}.{ext}').convert_alpha()
            if face in ['right', 'left', 'front', 'back']:
                texture = pygame.transform.flip(texture, flip_x=True, flip_y=False)  # debug
            else:
                texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)  # debug
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=4, data=None)  # load in GLSL

        for i in range(6):
            texture_data = pygame.image.tostring(textures[i], 'RGBA')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def __get_depth_texture__(self) -> moderngl.DEPTH_TEST:
        depth_texture = self.ctx.depth_texture(config.SCREEN_size)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def __destroy__(self) -> None: [tex.release() for tex in self.textures.values()]


CustomTexture_name = Texture.name
