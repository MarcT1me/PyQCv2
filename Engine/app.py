""" Collection of utilities for working with the application class.
"""
from loguru import logger
# default
from abc import abstractmethod, ABC
from typing import Type, List, Dict, Self

# Engine import
import Engine
from Engine.graphic import err_screen


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
    WorkAppType: Self = Engine.EMPTY
    win = Engine.graphic.Graphics

    """ Error catching """
    failures: List[Engine.failures.Failure] = []
    """ Timing """
    clock: Engine.timing.Clock = Engine.EMPTY
    """ Events """
    event_list: List[Engine.pg.event.EventType] = []
    key_list: Engine.pg.key.ScancodeWrapper = []
    joysticks: Dict[int, Engine.pg.joystick.JoystickType] = {}

    """ Scene and space context """
    root_scene: Engine.scene.Scene = Engine.EMPTY

    def __new__(cls, *args, **kwargs):
        """ creating App class """
        obj: App = super().__new__(cls)
        obj.__pre_init__(*args, **kwargs)
        Engine.graphic.Graphics.gl_data = obj.__gl_date__()
        Engine.graphic.Graphics.data = obj.__win_date__()
        return obj

    def __pre_init__(self, *args, **kwargs) -> None:
        """ Pre-initialisation Application. Before main __init__ """
        Engine.pg.init()
        Engine.data.File.load_engine_config('settings')  # general
        Engine.data.File.load_engine_config('graphics')  # graphics

    def __gl_date__(self) -> Engine.graphic.GlData:
        """ Pre-initialisation Graphic Libreary. Before main __init__ """
        return

    def __win_date__(self) -> Engine.graphic.WinData:
        """ Pre-initialisation main Window. Before main __init__ """

    def __init__(self, *args, **kwargs) -> None:
        """ Main app initialisation.
        in method realised init pygame, load config files and clock
         use supper()
         """
        # timing
        App.clock = Engine.timing.Clock()
        # window
        Engine.graphic.Graphics()

        logger.success('ENGINE - INIT\n')

    def __post_init__(self, *args, **kwargs) -> None:
        """ Post initialisation, after main __init__ """
        ...

    def __repr__(self) -> str:
        return f'<class: App; running={self.running}>'

    def __str__(self) -> str:
        return f'{"running" if self.running else "stoped"} App'

    @abstractmethod
    def events(self) -> None:
        """ handle all events """
        ...

    @abstractmethod
    def pre_update(self) -> None:
        """ UpDate application"""
        ...

    @abstractmethod
    def update(self) -> None:
        """ UpDate application"""
        ...

    @abstractmethod
    def pre_render(self) -> None:
        """ render all app surfaces, and use engine render methods """
        ...

    @abstractmethod
    def render(self) -> None:
        """ render all app surfaces, and use engine render methods """
        ...

    def run(self) -> None:
        """ Run game.
        The method that starts the event loop.
        This is a while loop that uses the current variable in the App class field as a condition. 3 methods are
        called in the loop itself: events, update_app, update_window
        
        :return: Nothing
        :raises KeyboardInterrupt: if the cycle is not completed correctly.
        """
        # after main.init
        self.__post_init__()
        """ Main-loop """
        while self.running:
            # events
            App.event_list = Engine.pg.event.get()
            App.key_list = Engine.pg.key.get_pressed()
            self.events()
            Engine.threading.Thread.waiting_pending()
            Engine.threading.Thread.wait_worked()
            # update
            self.pre_update()
            Engine.threading.Thread.waiting_pending()
            Engine.threading.Thread.wait_worked()
            self.update()
            Engine.threading.Thread.waiting_pending()
            Engine.threading.Thread.wait_worked()
            # render
            self.pre_render()
            Engine.threading.Thread.waiting_pending()
            Engine.threading.Thread.wait_worked()
            self.render()
            # clok tick
            App.clock.tick(Engine.data.Win.fps)

    @staticmethod
    def on_failure(err: Engine.failures.Failure) -> None:
        """ calling, if got exception in mainloop """
        App.failures.append(err)
        if err.critical:
            App.running = False
        print('\n\n')
        logger.exception(err)

    @staticmethod
    def on_exit() -> None:
        for err in tuple(App.failures):
            if not err.critical:
                App.failures.remove(err)

        Engine.graphic.Graphics.__release__()
        Engine.pg.quit()

        logger.success('ENGINE - QUIT\n\n')


def mainloop(app: Type[App]) -> None:
    """
    :param app: application class with initializer
    :return: Last worked app
    :raise AssertionError: if there are problems with the argument
    """
    assert issubclass(app, App), 'Arg `app` must be inherited by `Engine.app.App`'
    App.WorkAppType = app

    work_app: App = app  # current app object
    while App.running:
        with Engine.failures.Catch(identifier=f"{mainloop}_Catch__ENGINE__"):
            work_app = app()
            work_app.run()
        if work_app:
            work_app.on_exit()
        if App.failures:
            # show err window
            App.running = err_screen.show_window() if Engine.data.Main.IS_RELEASE \
                else err_screen.show_traceback()
            App.failures.clear()
    # end mainloop
    return work_app
