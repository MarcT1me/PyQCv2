import Engine
from Engine.app import App, EventThread
from loguru import logger


class TestApp(App):
    def __pre_init__(self) -> None:
        # load config file
        Engine.data.File.reed_data()
        Engine.data.File.fill_default_data()

    @staticmethod
    def __win_data__() -> Engine.graphic.WinData:
        # set Window Data
        return Engine.graphic.WinData(
            name="Main Window",
            flags=Engine.data.Win.flags | Engine.pg.OPENGL
        )

    def __init__(self) -> None:
        super().__init__()
        self.fps_font = Engine.pg.font.SysFont("Arial", 30)
        self.rnd_fps_font: Engine.pg.Surface = None

    @Engine.decorators.deferrable_threadsafe
    @Engine.decorators.single_event
    @Engine.decorators.multithread(thread_class=EventThread)
    def events(self, *, event, thread) -> None:
        if event.type == Engine.pg.KEYDOWN:
            if event.key == Engine.pg.K_ESCAPE:
                App.running = False
            elif event.key == Engine.pg.K_g:
                raise Exception("Test exception")
            elif event.key == Engine.pg.K_t:
                Engine.threading.Thread(action=lambda: print("Hello from thread")).start()

        self.default_event_handling(self, event=event)

    def pre_update(self) -> None:
        ...

    def update(self) -> None:
        ...

    def pre_render(self) -> None:
        if self.clock.timer("fps_timer", 1 / 3):
            self.rnd_fps_font = self.fps_font.render(
                f"fps: {int(round(self.clock.get_fps(), 0))}, "
                f"interface_type: {self.graphic.gl_data.interface_type.__name__}",
                True, "white"
            )

    @Engine.decorators.gl_render
    def render(self) -> None:
        with self.graphic.interface as interface:
            interface.surface.blit(self.rnd_fps_font, (0, 0))

    @staticmethod
    def on_failure(err: Engine.failures.Failure) -> None:
        App.on_failure(err)

    @staticmethod
    @Engine.decorators.dev_only()
    def on_exit_print() -> None:
        logger.debug("exiting from App")

    @staticmethod
    def on_exit() -> None:
        App.on_exit()
        TestApp.on_exit_print()


if __name__ == "__main__":
    App.mainloop(TestApp)
