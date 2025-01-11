from loguru import logger
import os
import subprocess
from Engine.data.config import File, Main

__copy_arr = {
    # engine
    "": ("Engine\\data", {
        'graphics.engconf',
        'settings.engconf',
        'Logo.png'
    }),
    "default_project": ("", {
        '.gitignore',
        'main.py',
        'README.md',
        'requirements.txt'
    }),
    "default_project\\presets": ("presets", {
        'Logo.png'
    })
}


def __copy(dir: str, path: str, files: set[str]):
    os.makedirs(f'{File.APPLICATION_path}\\{path}')
    for file in files:
        with open(f"{File.__ENGINE_DATA__}\\{dir}\\{file}", "rb") as f1:
            with open(f"{File.APPLICATION_path}\\{path}\\{file}", "wb") as f2:
                f2.write(f1.read())


def create_project():
    logger.debug("CREATING ENGINE PROJECT")
    try:
        for d, (p, f) in __copy_arr:
            __copy(dir=p, path=p, files=f)
        os.makedirs(rf'{File.APPLICATION_path}/presets')

        logger.debug("Creating VirtualEnv")
        subprocess.run(f"python -m venv {File.APPLICATION_path}")
        subprocess.run(f"{File.APPLICATION_path}\\venv\\Scripts\\activate")
        logger.success("VirtualEnv created")

        logger.debug("Adding link on Engine")
        subprocess.run(f"mklink /D {File.APPLICATION_path}\\venv\\Lib\\site-package\\Engine "
                       f"{File.__ENGINE_DATA__.replace('/data', '')}")
        logger.success("link created")

        logger.debug("downloading requirements")
        subprocess.run("pip install -r requirements.txt")
        logger.success("PROJECT CREATED")

        logger.debug("starting PyCharm")
        subprocess.run(f"pycharm {File.APPLICATION_path}")
        logger.success("PyCharm started")

    except Exception as e:
        logger.exception(e.args[0])
    return start()


def build(*, patch: str = File.APPLICATION_path, name: str = 'main.pyw'):
    File.load_engine_config("settings")
    if not Main.IS_RELEASE:
        logger.debug("start changing configs")
        with open(rf'{patch}/Engine/data/settings.engconf', 'r') as f_r:
            data = ''.join(map(
                lambda l: 'Main.IS_RELEASE = YES  # YES\n' if 'IS_RELEASE' in l else l,
                f_r.readlines()
            ))
        with open(rf'{patch}/Engine/data/settings.engconf', 'w') as f_w:
            f_w.write(data)
        logger.success("configs changed")

    logger.debug("create cmd")
    cmd = f'pyinstaller --name \"{Main.APPLICATION_name}\" ' + \
          f'--icon=\"{patch}/{File.APPLICATION_ICO_dir}/{File.APPLICATION_ICO_name}\" ' + \
          f'--add-data \"C:/Program Files/Python311/Lib/site-packages/glcontext;glcontext\" ' + \
          f'--add-data \"C:/Program Files/Python311/Lib/site-packages/toml;toml\" ' + \
          f'--add-data \"{patch}/Engine/data;../Engine/data\" ' + \
          f'--add-data \"{patch}/presets;../presets\" ' + \
          f'\"{patch}/{name}\"'

    logger.debug("start compiling")
    result = subprocess.run(cmd, capture_output=True, text=True, check=False, shell=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    logger.success("success compile")


class start:
    def __add__(self, other):
        logger.debug("START AFTER CREATING\n")
        subprocess.run("python main.pyw")
