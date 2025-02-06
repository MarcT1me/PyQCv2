""" Collection of utilities for working with the application class.
"""
from loguru import logger
# default
from abc import abstractmethod, ABC
from typing import Type, List, Dict, Self, TYPE_CHECKING, final

# Engine import
import Engine
from Engine.graphic import err_screen


class EventThread(Engine.threading.Thread):
    """ Thread class for Handling GUI Events """
    _roster: Engine.arrays.Roster[str, Engine.threading.Thread] = Engine.threading.Thread.create_roster()


class PreUpdateThread(Engine.threading.Thread):
    """ Thread class for pre updating app """
    _roster: Engine.arrays.Roster[str, Engine.threading.Thread] = Engine.threading.Thread.create_roster()


class UpdateThread(Engine.threading.Thread):
    """ Thread class for updating app """
    _roster: Engine.arrays.Roster[str, Engine.threading.Thread] = Engine.threading.Thread.create_roster()


class PreRenderThread(Engine.threading.Thread):
    """ Thread class for pre rendering app """
    _roster: Engine.arrays.Roster[str, Engine.threading.Thread] = Engine.threading.Thread.create_roster()


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
    graphics: Engine.graphic.System = Engine.EMPTY
    audio: Engine.audio.System = Engine.EMPTY
    clock: Engine.timing.Clock = Engine.EMPTY

    """ Error catching """
    failures: List[Engine.failures.Failure] = []

    """ Events """
    event_list: List[Engine.pg.event.EventType] = []
    key_list: Engine.pg.key.ScancodeWrapper = []
    joysticks: Dict[int, Engine.pg.joystick.JoystickType] = {}

    """ Scene and space context """
    root_scene: Engine.objects.Scene = Engine.EMPTY

    @final
    def __init_subclass__(cls, **kwargs):
        Engine.data.File.load_engine_config('settings')  # general
        Engine.data.File.load_engine_config('graphics')  # graphics
        super().__init_subclass__()

    @final
    def __new__(cls, *args, **kwargs):
        """ creating App class """
        obj: App = super().__new__(cls)
        obj.__pre_init__()  # pre-init
        Engine.pg.init()
        # init systems
        App.graphics = Engine.graphic.System
        App.graphics()
        App.audio = Engine.audio.System()
        App.clock = Engine.timing.Clock()
        logger.success('ENGINE - INIT\n')
        return obj

    @abstractmethod
    def __pre_init__(self) -> None:
        """ Just app Pre-initialisation. Before main __init__ """

    @staticmethod
    @abstractmethod
    def __win_date__() -> Engine.graphic.WinData:
        """ Pre-initialisation main Window. Before main __init__ """

    @staticmethod
    def __gl_date__() -> Engine.graphic.GlData:
        """ Pre-initialisation Graphic Libreary. Before main __init__ """
        return Engine.graphic.GlData() if App.graphics.win_data.flags & Engine.pg.OPENGL else None

    def __init__(self) -> None:
        """ Just app initialisation. """

    @abstractmethod
    def __post_init__(self) -> None:
        """ Post initialisation, after main __init__
        Note: use supper first! """
        methods_to_defer = ["events", "pre_update", "update", "pre_render", "render"]

        for method_name in methods_to_defer:
            method = getattr(App.InheritedСlass, method_name)

            if not hasattr(method, "__is_deferred__"):
                deferred_method = Engine.decorators.deferrable(method)
                setattr(App.InheritedСlass, method_name, deferred_method)

    def __repr__(self) -> str:
        return f'<App: {Engine.data.Main.APPLICATION_name} (running={self.running}, failures={self.failures})>'

    @Engine.decorators.with_store(already_handled=False)
    @Engine.decorators.window_event(already_single=True)
    @final
    def default_event_handling(self, *, event: Engine.pg.event.Event, window: int | None):
        """ Engine default event handling """
        if self.default_event_handling.already_handled:
            self.default_event_handling.already_handled = False
            return

        if event.type == Engine.pg.QUIT:
            App.running = False
        elif event.type == Engine.pg.WINDOWRESIZED:
            if window:
                ...
            else:
                App.graphics.win_data.extern({"size": Engine.math.vec2(event.x, event.y)})
                self.events.defer(App.graphics.resset)
        elif event.type == Engine.pg.WINDOWMOVED:
            if window:
                ...
        elif event.type == Engine.pg.WINDOWDISPLAYCHANGED:
            if window:
                ...
            else:
                App.graphics.win_data.extern({"monitor": event.display_index})
        elif event.type == Engine.pg.JOYDEVICEADDED:
            joy = Engine.pg.joystick.Joystick(event.device_index)
            App.joysticks[joy.get_instance_id()] = joy
        elif event.type == Engine.pg.JOYDEVICEREMOVED:
            del App.joysticks[event.instance_id]
        elif event.type == Engine.pg.AUDIODEVICEADDED:
            ...
        elif event.type == Engine.pg.AUDIODEVICEREMOVED:
            ...

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
            App.event_list = Engine.pg.event.get()
            App.key_list = Engine.pg.key.get_pressed()

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
            App.clock.tick(Engine.data.Win.fps)

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

        Engine.graphic.System.__release__()
        Engine.pg.quit()

        logger.success('ENGINE - QUIT\n\n')


def mainloop(app: Type[App]) -> None:
    """
    :param app: application class with initializer
    :return: Last worked app
    :raise AssertionError: if there are problems with the argument
    """
    assert issubclass(app, App), 'Arg `app` must be inherited by `Engine.app.App`'
    App.InheritedСlass = app

    while App.running:
        with Engine.failures.Catch(identifier=f"{mainloop}_Catch__ENGINE__"):
            App.WorkingInstance = app()
            App.WorkingInstance.run()
        if App.WorkingInstance:
            App.WorkingInstance.on_exit()
        if App.failures:
            # show err window
            App.running = err_screen.show_window() if Engine.data.Main.IS_RELEASE \
                else err_screen.show_traceback()
            App.failures.clear()
