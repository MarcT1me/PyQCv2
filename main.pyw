import Engine
from Engine.app import App
from loguru import logger


class TestApp(App):
    def __pre_init__(self, *args, **kwargs) -> None:
        super().__pre_init__()
        # load config file
        Engine.data.File.reed_data()
        Engine.data.File.fill_default_data()

        Engine.data.Win.fps = 30

    def __win_date__(self) -> Engine.graphic.WinData:
        # set Window Data
        return Engine.graphic.WinData(
            flags=Engine.data.Win.flags | Engine.pg.OPENGL
        )

    def __gl_date__(self) -> Engine.graphic.GlData:
        return Engine.graphic.GlData()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        App.win.set_icon(
            Engine.pg.image.load(
                f"{Engine.data.File.APPLICATION_path}\\{Engine.data.File.APPLICATION_ICO_dir}"
                f"\\{Engine.data.File.APPLICATION_ICO_name}"
            )
        )

        self.fps_font = Engine.pg.font.SysFont("Arial", 30)
        self.rnd_fps_font: Engine.pg.Surface = None
        self.video_changed: bool = False

    @Engine.decorators.multithread
    @Engine.decorators.single_event
    def events(self, event) -> None:
        if event.type == Engine.pg.QUIT:
            App.running = False
        elif event.type == Engine.pg.KEYDOWN:
            if event.key == Engine.pg.K_ESCAPE:
                App.running = False
            elif event.key == Engine.pg.K_g:
                raise Exception("Test exception")
        elif event.type == Engine.pg.VIDEORESIZE:
            Engine.threading.Thread.set_important()
            App.win.data.extern({"size": Engine.math.vec2(event.size)})
            self.video_changed = True
            Engine.threading.Thread.mute_important()

    def pre_update(self) -> None:
        if self.video_changed:
            App.win.resset()
            self.video_changed = False

    def update(self) -> None:
        ...

    def pre_render(self) -> None:
        if self.clock.timer("fps_timer", 1 / 3):
            self.rnd_fps_font = self.fps_font.render(
                f"fps: {int(round(self.clock.get_fps(), 0))}, "
                f"interface_type: {Engine.graphic.Graphics.gl_data.interface_class.__name__}",
                True, "white"
            )

    @Engine.decorators.gl_render
    def render(self) -> None:
        with Engine.graphic.Graphics.interface as interface:
            interface.surface.blit(self.rnd_fps_font, (0, 0))

    @staticmethod
    def on_failure(err: Engine.failures.Failure) -> None:
        App.on_failure(err)

    @staticmethod
    @Engine.decorators.dev_only
    def on_exit_print() -> None:
        logger.debug("exiting from App")

    @staticmethod
    def on_exit() -> None:
        App.on_exit()
        TestApp.on_exit_print()


if __name__ == "__main__":
    Engine.app.mainloop(TestApp)
