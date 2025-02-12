from typing import Any, Optional

import toml

import Engine
from Engine.app import App, EventThread
from loguru import logger


class TomlConfigLoader(Engine.assets.AssetLoader):
    def load(self, asset_file: 'Engine.assets.AssetFileData') -> Any:
        return asset_file.path.open()

    def create(
            self, asset_file: 'Engine.assets.AssetFileData', dependencies: 'Optional[list[Engine.assets.LoadedAsset]]',
            content: Any
    ) -> 'Engine.assets.AssetData':
        config = Engine.assets.ConfigData(
            name=asset_file.name,
            data=toml.load(content)
        )
        config.setdefault(
            category_name="Win",
            defaults={'fps': Engine.data.WinDefault.fps,
                      'size': Engine.math.vec2(Engine.data.WinDefault.size),
                      'vsync': Engine.data.WinDefault.vsync,
                      'full': Engine.data.WinDefault.full,
                      'monitor': Engine.data.WinDefault.monitor}
        )
        config.setdefault(category_name='Core', defaults={})

        return config


class TestApp(App):
    def __pre_init__(self, assets_type_configs: list[Engine.assets.AssetLoader]) -> None:
        # adding config asset type
        assets_type_configs.extend([
            TomlConfigLoader(
                Engine.assets.AssetType(Engine.assets.MajorType.Toml, Engine.assets.MinorType.Config)
            )
        ])
        super().__pre_init__(assets_type_configs)  # init asset manager

        logger.debug(f"asset roster {App.assets.storage.__dict__}")

        # loading config
        self.main_config: Engine.assets.LoadedAsset = App.assets.load(
            Engine.assets.AssetFileData(
                name=Engine.data.FileSystem.config_name,
                type=Engine.assets.AssetType(Engine.assets.MajorType.Toml, Engine.assets.MinorType.Config),
                path=f"{Engine.data.FileSystem.data_path()}\{Engine.data.FileSystem.config_name}.toml"
            )
        )
        print(self.main_config.asset_data)

    @staticmethod
    def __win_data__() -> Engine.graphic.WinData:
        main_config_asset: Engine.assets.AssetData = App.assets.storage.TomlConfig.definite(
            Engine.data.FileSystem.config_name)
        # set Window Data from config
        return Engine.graphic.WinData(
            name="Main Window",
            size=main_config_asset.data["Win"]["size"],
            # vsync=main_config_asset.data["Win"]["vsync"],
            # full=main_config_asset.data["Win"]["full"],
            # is_desktop=main_config_asset.data["Win"]["is_desktop"],
            flags=Engine.data.WinDefault.flags | Engine.pg.OPENGL
        )

    def __init__(self) -> None:
        super().__init__(
            self.main_config.data["Win"]["fps"]
        )  # init engine

        # create font surface and font
        self.fps_font = Engine.pg.font.SysFont("Arial", 30)
        self.rnd_fps_font: Engine.pg.Surface = None

        # load music
        self.clip = Engine.audio.Clip(
            f"{Engine.data.FileSystem.APPLICATION_path}\\{Engine.data.FileSystem.AUDIO_dir}\\10. Crest.mp3"
        )

    def __post_init__(self) -> None:
        super().__post_init__()  # post-init engine

        # play music in loop (100 times)
        App.audio.active_devices.output.just.play(self.clip, loops=100)

    @Engine.decorators.deferrable_threadsafe
    @Engine.decorators.single_event
    @Engine.decorators.multithread(thread_class=EventThread)
    def events(self, *, event, thread) -> None:
        # handle events
        if event.type == Engine.pg.KEYDOWN:
            if event.key == Engine.pg.K_ESCAPE:
                App.running = False
            elif event.key == Engine.pg.K_g:
                raise Exception("Test exception")
            elif event.key == Engine.pg.K_t:
                Engine.threading.Thread(action=lambda: print("Hello from thread")).start()

        self.event.handle_default(self.event, event=event)  # default event handling

    def pre_update(self) -> None:
        # pre-update app
        ...

    def update(self) -> None:
        # update app data
        ...

    def pre_render(self) -> None:
        # pre-render. Changing surfaces and other data for rendering
        if self.clock.timer("fps_timer", 1 / 3):
            self.rnd_fps_font = self.fps_font.render(
                f"fps: {int(round(self.clock.get_fps(), 0))}, "
                f"interface_type: {self.graphic.gl_data.interface_type.__name__}",
                True, "white"
            )

    @Engine.decorators.gl_render
    def render(self) -> None:
        # main render linear algorithm
        ...
        # render interface linear algorithm
        with self.graphic.interface as interface:
            interface.surface.blit(self.rnd_fps_font, (0, 0))

    @staticmethod
    def on_failure(err: Engine.failures.Failure) -> None:
        # handling errors
        App.on_failure(err)

    @staticmethod
    @Engine.decorators.dev_only()
    def on_exit_print() -> None:
        # debug logging (only in debug mode)
        logger.debug("exiting from App")

    @staticmethod
    def on_exit() -> None:
        # release game and engine data
        App.on_exit()
        TestApp.on_exit_print()


if __name__ == "__main__":
    TestApp.mainloop()  # start app mainloop
