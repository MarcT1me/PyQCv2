""" Engine settings and configs
"""
from typing import final
import os
from inspect import stack

from loguru import logger

import Engine

@final
class MainData:
    """ Main engine constants """
    IS_RELEASE: bool = False
    # string
    APPLICATION_name = "QuantumApp"
    APPLICATION_version = "DEV-0.0.0"


@final
class WinDefault:
    """ Screen settings """
    # main window
    size: tuple = Engine.math.vec2(720, 480)
    monitor: int = None
    title: str = MainData.APPLICATION_name + " Window"
    vsync: bool = False
    full: bool = False
    is_desktop: bool = False
    flags: int = Engine.pg.DOUBLEBUF
    fps: int = 0


@final
class FileSystem:
    """ File and path data """

    # global paths
    __ENGINE_DATA__: str = os.path.dirname(os.path.abspath(__file__)).removesuffix(r'\PyInstaller\loader')
    APPLICATION_path: str = os.path.dirname(os.path.abspath(stack()[-1].filename)).removesuffix(r'\PyInstaller\loader')
    APPDATA_LOCAL_path: str = rf'{os.path.expanduser("~")}\AppData\Local'

    # Directory names
    ENGINE_DATA_DIR: str = f'Engine\\data'
    PRESETS_dir: str = "presets"
    ENGINE_SHADER_dir: str = f'{ENGINE_DATA_DIR}\\{PRESETS_dir}\\shaders'
    DATA_dir: str = "gamedata"
    SHADER_dir: str = "shaders"
    TEXTURE_dir: str = "textures"
    AUDIO_dir: str = "audio"

    # config and other data
    config_name: str = 'main_config'
    config_local_dir: bool = True
    data_path: Engine.FUNC = lambda: (FileSystem.APPLICATION_path if FileSystem.config_local_dir
                                      else FileSystem.APPDATA_LOCAL_path) + "\\" + FileSystem.DATA_dir

    # ico settings
    APPLICATION_ICO_dir: str = f'Engine/data'
    APPLICATION_ICO_name: str = 'Service.png'

    # engine configs (*.engconf)
    @staticmethod
    def load_engine_config(name: str) -> None:
        path: str = f"{FileSystem.APPLICATION_path}\\{FileSystem.ENGINE_DATA_DIR}\\{name}.engconf"
        logger.info(f'load Engine configs from {path}')

        # reading
        with open(path, 'r') as config_file:
            lines_data = config_file.read()

        data = ''.join(lines_data)
        with Engine.failures.Catch(identifier=f"{FileSystem.load_engine_config}_Catch__ENGINE__"):
            exec(data)
        logger.success(f'apply Engine configs from {name} eng-config')
