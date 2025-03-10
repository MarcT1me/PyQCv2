from Engine.data.config import FileSystem, MainData
from loguru import logger
import subprocess
import os

__copy_arr = {
    (
        "",  # from (start from Engine\\data)
        "Engine\\data", (  # where (start from target path)
            'settings.engconf',  # what
            'graphics.engconf',
        )
    ),
    (
        "default_project",
        "", (
            '.gitignore',
            'main.py',
            'README.md',
            'requirements.txt',
        )
    ),
    (
        "default_project\\gamedata",
        "gamedata", (
            'main_config.toml',
        )
    ),
    (
        "default_project\\presets",
        "presets", (
            'Logo.png',
        )
    ),
    (
        "default_project\\presets\\audio",
        "presets\\audio", (
            '10. Crest.mp3',
        )
    )
}


def __copy(directory: str, path: str, files: tuple[str]):
    if not os.path.exists(f'{FileSystem.APPLICATION_path}\\{path}'):
        os.makedirs(f'{FileSystem.APPLICATION_path}\\{path}')
    for file in files:
        with open(f"{FileSystem.ENGINE_DATA_path}\\{directory}\\{file}", "rb") as f1:
            with open(f"{FileSystem.APPLICATION_path}\\{path}\\{file}", "wb") as f2:
                f2.write(f1.read())


def create_project():
    logger.debug("CREATING ENGINE PROJECT")
    try:
        for d, p, f in __copy_arr:
            __copy(directory=d, path=p, files=f)

        logger.debug("Creating VirtualEnv")
        print(f"python -m venv \"{FileSystem.APPLICATION_path}\\venv\"")
        subprocess.run(f"python -m venv \"{FileSystem.APPLICATION_path}\\venv\"", shell=True)
        logger.success("VirtualEnv created")

        logger.debug("Adding link on Engine")
        print(f"mklink /D \"{FileSystem.APPLICATION_path}\\venv\\Lib\\site-packages\\Engine\" "
              f"\"{FileSystem.ENGINE_DATA_path[:-5]}\"")
        subprocess.run(f"mklink /D \"{FileSystem.APPLICATION_path}\\venv\\Lib\\site-packages\\Engine\" "
                       f"\"{FileSystem.ENGINE_DATA_path[:-5]}\"", shell=True, check=True)
        logger.success("link created")

        logger.debug("downloading requirements")
        print(f"\"{FileSystem.APPLICATION_path}\\venv\\Scripts\\pip\" install -r requirements.txt")
        subprocess.run(f"\"{FileSystem.APPLICATION_path}\\venv\\Scripts\\pip\" install -r requirements.txt", shell=True)
        logger.success("PROJECT CREATED")

        try:
            logger.debug("starting PyCharm")
            print(f"pycharm {FileSystem.APPLICATION_path}")
            subprocess.run(f"pycharm \"{FileSystem.APPLICATION_path}\"", shell=True)
            logger.success("PyCharm started")
        except Exception as e:
            logger.warning("Cant lunch PyCharm.")

    except Exception as e:
        logger.exception(e.args[0])


def build(path: str = FileSystem.APPLICATION_path, name: str = 'main.py', ico_name: str = None):
    FileSystem.load_engine_config("settings")
    if not MainData.IS_RELEASE:
        logger.debug("start changing configs")
        with open(rf'{path}/Engine/data/settings.engconf', 'r') as f_r:
            data = ''.join(map(
                lambda l: 'Main.IS_RELEASE = YES  # YES\n' if 'IS_RELEASE' in l else l,
                f_r.readlines()
            ))
        with open(rf'{path}/Engine/data/settings.engconf', 'w') as f_w:
            f_w.write(data)
        logger.success("configs changed")

    logger.debug("create cmd")
    cmd = f'pyinstaller --name \"{MainData.APPLICATION_name}\" ' + \
          (
              f'--icon=\"{path}/{ico_name}\" '
              if ico_name else ""
          ) + \
          f'--add-data \"C:/Program Files/Python311/Lib/site-packages/glcontext;glcontext\" ' + \
          f'--add-data \"C:/Program Files/Python311/Lib/site-packages/toml;toml\" ' + \
          f'--add-data \"{path}/Engine/data;../Engine/data\" ' + \
          f'--add-data \"{path}/presets;../presets\" ' + \
          f'\"{path}/{name}\"'

    logger.debug("start compiling")
    print(cmd)
    # result = subprocess.run(cmd, capture_output=True, text=True, check=False, shell=True)
    # if result.returncode != 0:
    #     raise RuntimeError(result.stderr)
    logger.success("success compile")


def git_commit(message: str):
    FileSystem.load_engine_config('settings')  # general
    cmd: str = f"git commit -m \"{MainData.APPLICATION_version}  // {message}\""
    print(cmd)
