from typing import Optional, TextIO
from dataclasses import dataclass
import toml

import Engine
from Engine.app import App, EventThread
from loguru import logger


class TomlConfigLoader(Engine.assets.AssetLoader):
    def load(self, asset_file: Engine.assets.AssetFileData) -> TextIO:
        return asset_file.path.open()

    def create(
            self, asset_file: Engine.assets.AssetFileData, dependencies: Optional[list[Engine.assets.LoadedAsset]],
            content: TextIO
    ) -> Engine.assets.ConfigData:
        config = Engine.assets.ConfigData(
            id=asset_file.id,
            content=toml.load(content)
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


@dataclass(kw_only=True)
class TestAppData(Engine.app.AppData):
    main_config: Engine.assets.ConfigData


class TestApp(App):
    deta: TestAppData
    # TestAppData
    main_config: Engine.assets.ConfigData

    @classmethod
    def __pre_init__(cls) -> None:
        # adding config asset type
        assets_type_configs = [
            TomlConfigLoader(
                Engine.assets.AssetType(Engine.DataType.Toml | Engine.DataType.Config)
            ),
        ]
        cls.init_asset_manager(assets_type_configs)  # init asset manager

        # loading config
        main_config: Engine.assets.LoadedAsset = App.assets.load(
            Engine.assets.AssetFileData(
                type=Engine.assets.AssetType(Engine.DataType.Toml | Engine.DataType.Config),
                path=f"{Engine.data.FileSystem.data_path()}\{Engine.data.FileSystem.config_name}.toml"
            )
        )

        return TestAppData(
            fps=main_config.data["Win"]["fps"],
            assets_type_configs=assets_type_configs,
            main_config=main_config
        )

    @staticmethod
    def __win_data__() -> Engine.graphic.WinData:
        main_config_asset: Engine.assets.ConfigData = App.assets.storage.TomlConfig.definite(
            Engine.data.FileSystem.config_name + ".toml"
        )
        # set Window Data from config
        return Engine.graphic.WinData(
            title="Main Window",
            size=main_config_asset.content["Win"]["size"],
            vsync=main_config_asset.content["Win"]["vsync"],
            full=main_config_asset.content["Win"]["full"],
            is_desktop=main_config_asset.content["Win"]["is_desktop"],
            flags=Engine.data.WinDefault.flags | Engine.pg.OPENGL
        )

    def __init__(self, data: TestAppData) -> None:
        super().__init__(data)  # init engine

        # create font surface and font
        self.fps_font = Engine.pg.font.SysFont("Arial", 30)
        self.rnd_fps_font: Engine.pg.Surface = None

        self.rnd_version_font = self.fps_font.render(
            f"APP INFO.  "
            f"Name: {Engine.data.MainData.APPLICATION_name},  "
            f"Version: {Engine.data.MainData.APPLICATION_version},  "
            f"IsRelease: {Engine.data.MainData.IS_RELEASE}",
            True, "white"
        )

        # load music
        self.clip = self.assets.load(
            Engine.assets.AssetFileData(
                type=Engine.DataType.AudioClip,
                path=f"{Engine.data.FileSystem.APPLICATION_path}\\{Engine.data.FileSystem.AUDIO_dir}\\Sf Fiksitinc.mp3"
            )
        )

    def __post_init__(self) -> None:
        super().__post_init__()  # post-init engine

        # play music in loop (100 times)
        App.audio.active_devices.output.just.play(self.clip.data)

    @Engine.decorators.deferrable_threadsafe
    @Engine.decorators.single_event
    @Engine.decorators.multithread(thread_class=EventThread)
    def events(self, *, event) -> None:
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
            interface.surface.blit(
                self.rnd_fps_font,
                (0, 0)
            )
            interface.surface.blit(
                self.rnd_version_font,
                (0, interface.surface.get_size()[1] - self.rnd_version_font.get_size()[1])
            )

    def on_failure(self, failure: Engine.failures.Failure) -> None:
        # handling errors
        if super().on_failure(failure) is Engine.ResultType.Finished: return

        # logger.debug(
        logger.error(f"App catch any failure: {failure.err}")

    @staticmethod
    @Engine.decorators.dev_only()
    def on_exit_print() -> None:
        # debug logging (only in debug mode)
        logger.debug("exiting from App")

    def on_exit(self) -> None:
        # release game and engine data
        super().on_exit()
        TestApp.on_exit_print()


if __name__ == "__main__":
    TestApp.mainloop()  # start app mainloop
