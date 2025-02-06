import Engine
from Engine.app import App
from loguru import logger


class QuantumApp(App):
    def __pre_init__(self, *args, **kwargs) -> None:
        super().__pre_init__()
        # load config file
        Engine.data.File.reed_data()
        Engine.data.File.fill_default_data()

    def __win_data__(self) -> Engine.graphic.WinData:
        # set Window Data
        return Engine.graphic.WinData(
            title="Gravity Simulation 3",
            size=Engine.math.vec2(1600, 900),
            flags=Engine.data.Win.flags | Engine.pg.OPENGL
        )

    def __gl_data__(self) -> Engine.graphic.GlData:
        return Engine.graphic.GlData(
            interface_type=Engine.graphic.HardInterface,
            view_start=Engine.math.vec2(0, 0)
        )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        Engine.graphic.System.set_icon(
            Engine.pg.image.load(
                f"{Engine.data.File.APPLICATION_path}\\{Engine.data.File.APPLICATION_ICO_dir}"
                f"\\{Engine.data.File.APPLICATION_ICO_name}"
            )
        )

        self.fps_font = Engine.pg.font.SysFont("Arial", 30)
        self.rnd_fps_font: Engine.pg.Surface = None

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
        elif event.type == Engine.pg.WINDOWRESIZED:
            Engine.graphic.System.win_data.extern(
                {
                    "size": Engine.math.vec2(event.x, event.y)
                }
            )
            Engine.graphic.System.set_viewport(
                Engine.math.vec4(*Engine.graphic.System.gl_data.view_start, *Engine.graphic.System.win_data.size)
            )
            Engine.graphic.System.resset()

    def pre_update(self) -> None:
        ...

    def update(self) -> None:
        ...

    def pre_render(self) -> None:
        if self.clock.timer("fps_timer", 1 / 1500):
            self.rnd_fps_font = self.fps_font.render(
                f"fps: {int(round(self.clock.get_fps(), 0))}, "
                f"interface_type: {Engine.graphic.System.gl_data.interface_type.__name__}",
                True, "white"
            )

    @Engine.decorators.gl_render
    def render(self) -> None:
        with Engine.graphic.System.interface as interface:
            interface.surface.blit(self.rnd_fps_font, (0, 0))

    @staticmethod
    def on_failure(err: Engine.failures.Failure) -> None:
        App.on_failure(err)

    @Engine.decorators.dev_only
    def on_exit_print(self) -> None:
        logger.debug("exiting from App")

    def on_exit(self) -> None:
        super().on_exit()
        self.on_exit_print()


if __name__ == "__main__":
    Engine.app.mainloop(QuantumApp)
