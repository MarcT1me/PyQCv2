from typing import Optional, TextIO
import toml

from loguru import logger

import Engine
from Engine.objects.iupdatable import IUpdatable


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
                      'size': Engine.math.ivec2(Engine.data.WinDefault.size),
                      'vsync': Engine.data.WinDefault.vsync,
                      'full': Engine.data.WinDefault.full,
                      'frameless': Engine.data.WinDefault.frameless,
                      'monitor': Engine.data.WinDefault.monitor}
        )
        config.setdefault(category_name='Core', defaults={})

        return config


class TestApp(Engine.App):
    def __pre_init__(self) -> None:
        # adding config asset type
        self.init_asset_manager(
            TomlConfigLoader(
                Engine.assets.AssetType(Engine.DataType.Toml | Engine.DataType.Config)
            ),
        )

        # loading config
        main_config: Engine.assets.ConfigData = self.assets.load(
            Engine.assets.AssetFileData(
                type=Engine.assets.AssetType(Engine.DataType.Toml | Engine.DataType.Config),
                path=f"{Engine.data.FileSystem.data_path()}\\{Engine.data.FileSystem.config_name}.toml"
            )
        ).asset_data

        with Engine.failures.Catch(identifier=f"{self.__pre_init__} Asset loading", is_critical=False,
                                   is_handling=False) as cth:
            init_clip: Engine.audio.Clip | Engine.ResultType.Error = cth.try_func(
                lambda: self.assets.load(
                    Engine.assets.AssetFileData(
                        type=Engine.DataType.AudioClip,
                        path=f"{Engine.data.FileSystem.APPLICATION_path}\\{Engine.data.FileSystem.AUDIO_dir}"
                             "\\Sf Fiksitinc.mp3"
                    )
                )
            )

        with Engine.failures.Catch(identifier="test scene updating", is_critical=False):
            # class for testing nodes
            class TestSceneNode(Engine.objects.SceneNode, IUpdatable):
                def update(self):
                    print(f"update {self.id}")
                    for child in self.iter_children():
                        if child.is_updatable(): child.update()

            """scene2"""
            scene2 = Engine.objects.Scene(
                Engine.objects.SceneNodeData(
                    id=Engine.data.Identifier("test scene 2"),
                )
            )

            # scene2 child1
            scene2_child_1 = TestSceneNode(
                Engine.objects.SceneNodeData(
                    id=Engine.data.Identifier("test scene2 child_1")
                )
            )
            scene2.add_child(scene2_child_1)

            """scene"""
            scene = Engine.objects.Scene(
                Engine.objects.SceneNodeData(
                    id=Engine.data.Identifier("test scene"),
                )
            )

            # scene2
            scene.add_child(scene2)

            # child1
            child_1 = TestSceneNode(
                Engine.objects.SceneNodeData(
                    id=Engine.data.Identifier("test scene child_1")
                )
            )
            child_1_1 = TestSceneNode(
                Engine.objects.SceneNodeData(
                    id=Engine.data.Identifier("test scene child_1_1")
                )
            )
            ret = scene.add_child(child_1)
            ret.add_child(child_1_1)

            # child2
            child_2 = TestSceneNode(
                Engine.objects.SceneNodeData(
                    id=Engine.data.Identifier("test scene child_2")
                )
            )
            scene.add_child(child_2)

            scene.update()

        return Engine.app.AppData(
            fps=main_config.content["Win"]["fps"],
            data_table=Engine.data.arrays.DataTable(
                main_config=main_config,
                init_clip=init_clip
            )
        )

    def __win_data__(self) -> Engine.graphic.WinData:
        main_config: Engine.assets.ConfigData = self.data_table.main_config
        # set Window Data from config
        return Engine.graphic.WinData(
            title=Engine.data.WinDefault.title,
            size=main_config.content["Win"]["size"],
            vsync=main_config.content["Win"]["vsync"],
            full=main_config.content["Win"]["full"],
            frameless=main_config.content["Win"]["frameless"],
            monitor=main_config.content["Win"]["monitor"],
            flags=Engine.data.WinDefault.flags | Engine.pg.OPENGL
        )

    def __init__(self) -> None:
        super().__init__()  # init engine

        # incorrect image loading
        self.qc_img = Engine.pg.transform.scale(Engine.pg.image.load(
            f"{Engine.data.FileSystem.APPLICATION_path}\\{Engine.data.FileSystem.PRESETS_dir}\\"
            "Logo.png"
        ), (600, 600))

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

        self.sound_chanel: Engine.audio.Channel = Engine.App.audio.active_devices.output.new_channel()

    def __post_init__(self) -> None:
        super().__post_init__()  # post-init engine

        # play music
        self.sound_chanel.play(self.data_table.init_clip.content)
        Engine.pg.event.clear(Engine.pg.WINDOWRESIZED)

    @Engine.decorators.deferrable_threadsafe
    @Engine.decorators.single_event
    @Engine.decorators.multithread(thread_class=Engine.threading.EventThread)
    def events(self, *, event) -> None:
        if event.type == Engine.pg.MOUSEMOTION:
            return
        else:
            print(event)
        # handle events
        if event.type == Engine.pg.KEYDOWN:
            if event.key == Engine.pg.K_ESCAPE:
                Engine.App.running = False
            elif event.key == Engine.pg.K_g:
                raise Engine.failures.Failure(err=Exception("Test exception"), critical=False)
            elif event.key == Engine.pg.K_t:
                Engine.threading.Thread(action=lambda: print("Hello from thread")).start()
            elif event.key == Engine.pg.K_F11:
                self.graphic.window.data.full = not self.graphic.window.data.full
                Engine.App.inherited.events.defer(
                    lambda: (
                        self.graphic.window.toggle_full(),
                        self.graphic.resset()
                    )
                )
        self.event.handle_default(event=event)  # default event handling

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
                f"interface_type: {self.graphic.gl_data.interface_type.__name__ if self.graphic.gl_data else None}",
                True, "white"
            )

    @Engine.decorators.gl_render
    def render(self) -> None:
        # main render linear algorithm
        ...
        # render interface linear algorithm
        with self.graphic.interface as interface:
            interface.blit(
                self.rnd_fps_font,
                (0, 0)
            )
            interface.blit(
                self.rnd_version_font,
                (0, interface.surface.get_size()[1] - self.rnd_version_font.get_size()[1])
            )

            interface.blit(
                self.qc_img,
                (350, 60)
            )

            Engine.pg.draw.circle(
                interface.surface, "red",
                Engine.pg.mouse.get_pos(),
                5
            )

    def on_failure(self, failure: Engine.failures.Failure) -> None:
        # handling errors
        if super().on_failure(failure) is Engine.ResultType.Finished: return
        # logger.debug(
        logger.error(f"App catch any failure: {failure.err}")

    @staticmethod
    @Engine.decorators.dev_only
    def on_exit_print() -> None:
        # debug logging (only in debug mode)
        logger.debug("exiting from App")

    def on_exit(self) -> None:
        # release game and engine data
        self.sound_chanel.stop()

        super().on_exit()
        TestApp.on_exit_print()


if __name__ == "__main__":
    TestApp.mainloop()  # start app mainloop
