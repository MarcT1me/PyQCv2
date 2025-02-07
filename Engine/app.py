""" Collection of utilities for working with the application class.
"""
from loguru import logger
# default
from abc import abstractmethod, ABC
from typing import Self, TYPE_CHECKING, final

# Engine import
import Engine
from Engine.graphic import err_screen


class EventThread(Engine.threading.Thread):
    """ Thread class for Handling GUI Events """
    _roster = Engine.threading.Thread.create_roster()


class PreUpdateThread(Engine.threading.Thread):
    """ Thread class for pre updating app """
    _roster = Engine.threading.Thread.create_roster()


class UpdateThread(Engine.threading.Thread):
    """ Thread class for updating app """
    _roster = Engine.threading.Thread.create_roster()


class PreRenderThread(Engine.threading.Thread):
    """ Thread class for pre rendering app """
    _roster = Engine.threading.Thread.create_roster()


class App(ABC):
    """
    Main App class.
    The main parent class for creating logic and running it in the main loop
    
    FEATURES
        it does not have an initializer to simplify inheritance and management
    
    METHODS
        1) events: Event method. Needs to be overwritten after inheritance:
        2) update_app: Updating program data. Needs to be overwritten after inheritance:
        3) update_window: Rendering of the program window. Needs to be overwritten after inheritance
        4) run: the main cycle of the program
        
    CLASS FIELD
        running (bool): a variable is a condition for the operation of the main loop
    """
    running: bool = True
    InheritedСlass: Self = Engine.EMPTY
    WorkingInstance: Self = Engine.EMPTY

    """ Systems """
    graphic: Engine.graphic.System = Engine.EMPTY
    audio: Engine.audio.System = Engine.EMPTY
    clock: Engine.timing.System = Engine.EMPTY
    event: Engine.events.System = Engine.EMPTY

    """ Error catching """
    failures: list[Engine.failures.Failure] = []

    """ Events """
    joysticks: dict[int, Engine.pg.joystick.JoystickType] = {}

    """ Scene and space context """
    root_scene: Engine.objects.Scene = Engine.EMPTY

    @final
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        # Engine configs
        Engine.data.File.load_engine_config('settings')  # general
        Engine.data.File.load_engine_config('graphics')  # graphics

        # deferrable functions
        for method_name in {"events", "pre_update", "update", "pre_render", "render"}:
            method = getattr(cls, method_name)
            if not hasattr(method, "__is_deferred__"):
                deferred_method = Engine.decorators.deferrable(method)
                setattr(cls, method_name, deferred_method)

    @final
    def __new__(cls, *args, **kwargs):
        """ creating App class """
        obj: App = super().__new__(cls)
        obj.__pre_init__()  # pre-init
        Engine.pg.init()
        # init systems
        App.graphic = Engine.graphic.System()
        App.audio = Engine.audio.System()
        App.clock = Engine.timing.System(Engine.data.Win.fps)
        App.event = Engine.events.System()

        logger.success('ENGINE - INIT\n')
        return obj

    def __pre_init__(self) -> None:
        """ Just app Pre-initialisation. Before main __init__ """

    @staticmethod
    @abstractmethod
    def __win_data__() -> Engine.graphic.WinData:
        """ Pre-initialisation main Window. Before main __init__ """

    @staticmethod
    def __gl_data__(win_data: Engine.graphic.WinData) -> Engine.graphic.GlData:
        """ Pre-initialisation Graphic Libreary. Before main __init__ """
        return Engine.graphic.GlData(win_data=win_data) if win_data.flags & Engine.pg.OPENGL else None

    def __init__(self) -> None:
        """ Just app initialisation. """
        self.graphic.__post_init__()
        print()

    def __post_init__(self) -> None:
        """ Post initialisation, after main __init__ """

    def __repr__(self) -> str:
        return f'<App: {Engine.data.Main.APPLICATION_name} (running={self.running}, failures={self.failures})>'

    # events
    if TYPE_CHECKING:
        @Engine.decorators.deferrable
        @Engine.decorators.single_event
        @Engine.decorators.window_event
        @Engine.decorators.multithread
        @abstractmethod
        def events(self) -> None:
            """ handle events """
            ...
    else:
        @abstractmethod
        def events(self) -> None:
            """ handle all events """
            ...

    # pre-update
    if TYPE_CHECKING:
        @Engine.decorators.deferrable
        @abstractmethod
        def pre_update(self) -> None:
            """ pre-update application dependencies for update"""
            ...
    else:
        @abstractmethod
        def pre_update(self) -> None:
            """ pre-update application dependencies for update"""
            ...

    # update
    if TYPE_CHECKING:
        @Engine.decorators.deferrable
        @abstractmethod
        def update(self) -> None:
            """ update application"""
            ...
    else:
        @abstractmethod
        def update(self) -> None:
            """ update application"""
            ...

    # pre-render
    if TYPE_CHECKING:
        @Engine.decorators.deferrable
        @abstractmethod
        def pre_render(self) -> None:
            """ render dependencies for render"""
            ...
    else:
        @abstractmethod
        def pre_render(self) -> None:
            """ render dependencies for render"""
            ...

    # render
    if TYPE_CHECKING:
        @Engine.decorators.deferrable
        @Engine.decorators.sdl_render
        @Engine.decorators.gl_render
        @Engine.decorators.window_event
        @abstractmethod
        def render(self) -> None:
            """ render all app surfaces, and use engine render methods """
            ...
    else:
        @abstractmethod
        def render(self) -> None:
            """ render all app surfaces, and use engine render methods """
            ...

    # running app
    def run(self) -> None:
        """ Run game.
        The method that starts the event loop.
        This is a while loop that uses the current variable in the App class field as a condition. 3 methods are
        called in the loop itself: events, update_app, update_window
        
        :return: Nothing
        :raises KeyboardInterrupt: if the cycle is not completed correctly.
        """
        self.__post_init__()
        """ Main-loop """
        while self.running:
            # events
            App.event.prepare()
            self.events(self)
            EventThread.wait()
            self.events.do_defer()

            # update
            self.pre_update(self)
            PreUpdateThread.wait()
            self.pre_update.do_defer()

            self.update(self)
            UpdateThread.wait()
            self.update.do_defer()

            # render
            self.pre_render(self)
            PreRenderThread.wait()
            self.pre_render.do_defer()

            self.render(self)
            self.render.do_defer()
            # clok tick
            App.clock.tick()

    @staticmethod
    def critical_failure(err):
        App.failures.append(err)
        App.running = False

    @staticmethod
    def on_failure(err: Engine.failures.Failure) -> None:
        """ calling, if got exception in mainloop """
        if err.critical:
            App.critical_failure(err)
        print('\n\n')
        logger.exception(err)

    @staticmethod
    def on_exit() -> None:
        for err in tuple(App.failures):
            if not err.critical:
                App.failures.remove(err)

        try:
            App.graphic.__release__()
        except AttributeError as exc:
            logger.error(f"can`t release graphic System, {exc.args[0]}")
        Engine.pg.quit()

        logger.success('ENGINE - QUIT\n')

    @classmethod
    def mainloop(cls) -> None:
        if not issubclass(cls, App):
            raise AttributeError('Arg `app` must be inherited by `Engine.app.App`')
        App.InheritedСlass = cls

        logger.info(
            f"Start App"
            f"name: {Engine.data.Main.APPLICATION_name}"
            f"version: {Engine.data.Main.APPLICATION_version}"
            f"at {'release' if Engine.data.Main.IS_RELEASE else 'debug'} mode"
        )

        while App.running:
            with Engine.failures.Catch(identifier=f"{App.mainloop}_Catch__ENGINE__") as c:
                App.WorkingInstance = cls()
                App.WorkingInstance.run()

            if KeyboardInterrupt in c.failures:
                logger.info("KeyboardInterrupt")
                return

            if App.WorkingInstance:
                App.WorkingInstance.on_exit()
            if App.failures:
                # show err window
                App.running = err_screen.show_window() if Engine.data.Main.IS_RELEASE \
                    else err_screen.show_window()
                App.failures.clear()
