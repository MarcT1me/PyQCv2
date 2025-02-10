""" Engine settings and configs
"""
from loguru import logger
# default
import os
from inspect import stack
from collections.abc import Mapping
# engine
import Engine
from Engine.arrays import AttributesKeeper


class Main:
    """ Main engine constants """
    IS_RELEASE: bool = False
    # string
    APPLICATION_name = "QuantumApp"
    APPLICATION_version = "DEV-0.0.0"
    ENGINE_name = "Engine"


@Engine.decorators.updatable
class Core(AttributesKeeper): pass


@Engine.decorators.updatable
class Win:
    """ Screen settings """
    # main window
    size: tuple = (720, 480)
    monitor: int = None
    name: str = Main.APPLICATION_name + ' | node window'
    vsync: bool = False
    full: bool = False
    is_desktop: bool = False
    flags: int = Engine.pg.DOUBLEBUF
    fps: int = 0

    update: 'ClassVar[classmethod[None, dict[str, Any]]]'  # type: ignore


class File:
    """ File and path data """
    config_name: str = 'config'
    config_ext: str = 'toml'
    config_local_dir: bool = True

    data: dict[str, dict] = {}
    # paths
    __ENGINE_DATA__: str = os.path.dirname(os.path.abspath(__file__)).removesuffix(r'\PyInstaller\loader')
    APPLICATION_path: str = os.path.dirname(os.path.abspath(stack()[-1].filename)).removesuffix(
        r'\PyInstaller\loader'
    ).removesuffix(
        rf"\{Main.ENGINE_name}\messages"
    )
    APPDATA_LOCAL_path: str = rf'{os.path.expanduser("~")}\AppData\Local'
    # names
    ENGINE_DATA_DIR: str = f'{Main.ENGINE_name}\\data'
    PRESETS_dir: str = "presets"
    ENGINE_SHADER_dir: str = f'{PRESETS_dir}\\shaders'
    DATA_dir: str = "gamedata"
    SHADER_dir: str = "shaders"
    TEXTURE_dir: str = "textures"
    AUDIO_dir: str = "audio"
    data_path: str = \
        lambda: (File.APPLICATION_path if File.config_local_dir else File.APPDATA_LOCAL_path) + "\\" + File.DATA_dir
    # ico settings
    APPLICATION_ICO_dir: str = f'{Main.ENGINE_name}/data'
    APPLICATION_ICO_name: str = 'Service.png'

    @staticmethod
    def change_data(changes: dict | Mapping, *, _data: dict = None) -> data:
        """ Change data in dict dict arg changes """
        for key, value in changes.items():
            File.data[key].update(value)
        return File.data

    # Working with config.* file
    @staticmethod
    def fill_default_data(
            set_default_core=lambda: File.data.setdefault('Core', {})
    ):
        _ = File.data.setdefault('Win', {})
        _ = File.data['Win'].setdefault('fps', Win.fps)
        _ = File.data['Win'].setdefault('size', Engine.math.vec2(Win.size))
        _ = File.data['Win'].setdefault('vsync', Win.vsync)
        _ = File.data['Win'].setdefault('full', Win.full)
        _ = File.data['Win'].setdefault('monitor', Win.monitor)
        set_default_core()

    @staticmethod
    def _load(_load_function) -> data:
        file_path = rf"{File.data_path()}\{File.config_name}.{File.config_ext}"
        try:
            with open(file_path, mode='r') as file:
                logger.info(f'load configs from {file_path}')
                return _load_function(file)
        except FileNotFoundError:
            File.fill_default_data()
            # create dir
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            # create file
            if not os.path.exists(file_path):
                f = open(file_path, 'w')
                exec(f"""from {File.config_ext} import dump; dump(File.data, f)""")
                f.close()
            logger.debug(f'file not fount -> create: {File.config_name}.{File.config_ext}')
            return File.data

    @staticmethod
    def _dump(_dump_function) -> None:
        file_path = rf"{File.data_path()}\{File.config_name}.{File.config_ext}"
        with open(file_path, mode='w') as file:
            _dump_function(File.data, file)
        logger.debug(f'dump configs in {file_path}')

    @classmethod
    def reed_data(cls) -> None:
        """ Apply data from file onto dict """

        if len(File.data) == 0:
            exec(f"""from {File.config_ext} import load; File.data = File._load(load)""")

        if "size" in File.data.get("Win", {}):
            File.data["Win"]["size"] = Engine.math.vec2(File.data["Win"]["size"])

        for key, value in File.data.items():
            getattr(getattr(Engine.data.config, key), "update")(value)

    @staticmethod
    def save_data() -> None:
        """ Write CONFIG files """

        if len(File.data) == 0:
            File.reed_data()

        exec(f"""from {File.config_ext} import dump; File._dump(dump)""")

    # Working with *.engconf
    @staticmethod
    def load_engine_config(name: str) -> None:
        logger.info(f'load Engine configs from {File.__ENGINE_DATA__}\\{name}.engconf')

        # reading
        with open(rf'{File.__ENGINE_DATA__}\{name}.engconf', 'r') as config_file:
            lines_data = config_file.read()

        data = ''.join(lines_data)
        with Engine.failures.Catch(identifier=f"{File.load_engine_config}_Catch__ENGINE__"):
            exec(data)
        logger.success(f'apply Engine configs from {name} eng-config')
