""" Collection of utilities for working with the application class.
"""
from loguru import logger
# default
from abc import abstractmethod, ABC
from typing import Self, TYPE_CHECKING, final, Optional

# Engine import
import Engine
from Engine.graphic import err_screen
from Engine.app.app_data import AppData


class EventThread(Engine.threading.Thread, Engine.failures.IFailureHandler):
    """ Thread class for Handling GUI Events """

    _roster: Engine.threading.ThreadRoster[str, Self] = Engine.threading.ThreadRoster()

    def on_failure(self, err: Engine.failures.Failure):
        logger.error("Failure catching from EventThread")
        App.instance.on_failure(err)


class PreUpdateThread(Engine.threading.Thread, Engine.failures.IFailureHandler):
    """ Thread class for pre updating app """

    _roster: Engine.threading.ThreadRoster[str, Self] = Engine.threading.ThreadRoster()

    def on_failure(self, err: Engine.failures.Failure):
        logger.error("Failure catching from PreUpdateThread")
        App.instance.on_failure(err)


class UpdateThread(Engine.threading.Thread, Engine.failures.IFailureHandler):
    """ Thread class for updating app """

    _roster: Engine.threading.ThreadRoster[str, Self] = Engine.threading.ThreadRoster()

    def on_failure(self, err: Engine.failures.Failure):
        logger.error("Failure catching from UpdateThread")
        App.instance.on_failure(err)


class PreRenderThread(Engine.threading.Thread, Engine.failures.IFailureHandler):
    """ Thread class for pre rendering app """

    _roster: Engine.threading.ThreadRoster[str, Self] = Engine.threading.ThreadRoster()

    def on_failure(self, err: Engine.failures.Failure):
        logger.error("Failure catching from PreRenderThread")
        App.instance.on_failure(err)


class App(ABC, Engine.data.MetaObject, Engine.failures.IFailureHandler):
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
    """ AppData object """
    data: AppData
    # AppData
    fps: int  # clock
    data_table: Engine.data.arrays.DataTable  # data
    assets_type_configs: list[Engine.assets.AssetLoader]  # assets
    failures: list[Engine.failures.Failure]  # Error catching
    joysticks: dict[int, Engine.pg.joystick.JoystickType]  # joysticks
    root_scene_object_id: Engine.data.Identifier  # Scene and space context
    # graphic data
    win_data: Engine.graphic.WinData
    gl_data: Optional[Engine.graphic.GL.GlData]

    """ The App class object Data """
    running: bool = True  # in App.running - Engine loop, in self.running - App loop
    # inherited app class and current app instance
    inherited: type[Self] = None
    instance: Self = None

    """ Engine Systems """
    # pre-init
    assets: Engine.assets.AssetManager = None
    # init
    clock: Engine.timing.System = None
    audio: Engine.audio.System = None
    event: Engine.events.System = None
    graphic: Engine.graphic.System = None

    """ Inherited App definition logic """

    @final
    def __init_subclass__(cls, **kwargs):
        """ creating App inherited class and loading Engine configs
        After all initializations """
        super().__init_subclass__()
        App.inherited = cls  # memorize inherited class
        # Engine configs
        Engine.data.FileSystem.load_engine_config('settings')  # general
        Engine.data.FileSystem.load_engine_config('graphics')  # graphics

        # set deferrable functions
        for method_name in {"events", "pre_update", "update", "pre_render", "render"}:
            method = getattr(cls, method_name)
            if not hasattr(method, "__is_deferred__"):
                deferred_method = Engine.decorators.deferrable(method)
                setattr(cls, method_name, deferred_method)

    def __repr__(self) -> str:
        return f'<App: {Engine.data.MainData.APPLICATION_name} (running={self.running}, failures={self.failures})>'

    """ __pre_init__ logic """

    @final
    def __new__(cls, *args, **kwargs):
        """ creating App class """
        App.instance = super().__new__(cls)  # memorize App instance
        return App.instance

    @classmethod
    @abstractmethod
    def __pre_init__(cls) -> AppData:
        """ App pre-initialisation.
        After lunching (inherited App.mainloop()).
        Before main __init__ logic.
        Using for init AppData and for initialization Asset Manager. """

    @staticmethod
    def init_asset_manager(assets_type_configs: list[Engine.assets.AssetLoader]) -> None:
        """ Initialize Asset manager.
        Need to use in __pre_init__.
        1) adding default assets types
        2) AssetManager.__init__ """
        assets_type_configs.extend([
            # Default Assets
            Engine.assets.asset_data.DefaultAssetLoader(
                Engine.assets.AssetType(Engine.DataType.Text | Engine.DataType.Asset)
            ),
            Engine.assets.asset_data.DefaultAssetLoader(
                Engine.assets.AssetType(Engine.DataType.Bin | Engine.DataType.Asset)
            ),
            # Audio Asset
            Engine.assets.audio_clip.AudioAssetLoader(
                Engine.assets.AssetType(Engine.DataType.AudioClip)
            ),
            # Shaders Assets
            Engine.assets.shader.GLSLShaderLoader(
                Engine.assets.AssetType(Engine.DataType.Text | Engine.DataType.Shader)
            ),
            Engine.assets.shader.GLSLShaderLoader(
                Engine.assets.AssetType(Engine.DataType.Bin | Engine.DataType.Shader)
            ),
            Engine.assets.shader.ShaderLoader(
                Engine.assets.AssetType(Engine.DataType.Shader)
            ),
        ])
        App.assets = Engine.assets.AssetManager(assets_type_configs)

    """ Main __init__ logic """

    @abstractmethod
    def __init__(self, data: AppData) -> None:
        """ Engine Initialization -> Initialization systems.
        Before inherited __pre_init__.
        Take AppData from the __pre_init__ """
        super().__init__(data)
        Engine.pg.init()
        # init systems
        App.clock = Engine.timing.System(data.fps)
        App.audio = Engine.audio.System()
        App.graphic = Engine.graphic.System()
        App.event = Engine.events.System()

        logger.success('ENGINE - INIT\n')

    @staticmethod
    @abstractmethod
    def __win_data__() -> Engine.graphic.WinData:
        """ Pre-initialisation -> Initialization main Window Data.
        After inherited __pre_init__ but in App.__init__ -> Engine.graphic.System.__init__ """

    @staticmethod
    def __gl_data__(win_data: Engine.graphic.WinData) -> Engine.graphic.GL.GlData:
        """ Pre-initialisation -> Initialization Graphic Libreary Data.
        After __win_data__
        Take WinData from the __win_data__"""
        return Engine.graphic.GL.GlData(win_data=win_data) if win_data.flags & Engine.pg.OPENGL else None

    """ App instance mainloop logic """

    def __post_init__(self) -> None:
        """ Engine post-initialisation.
        Before inherited __init__
        Calling in instance App.mainloop"""
        App.graphic.__post_init__()
        logger.success("APP - INIT\n")

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
        called in the loop itself: (pre-)events, (pre-)update, (pre-)render
        """
        self.__post_init__()

        logger.info("APP - START\n")
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

    """ App exit logic """

    @staticmethod
    def critical_failure(err):
        """ Using when app catch critical failure
        Already Implement in App.on_failure """
        App.instance.failures.append(err)
        App.running = False

    def on_failure(self, failure: Engine.failures.Failure) -> None:
        """ Calling when Ap got exception in mainloop """
        if isinstance(failure.err, KeyboardInterrupt):
            return Engine.ResultType.Finished

        if failure.critical:
            App.critical_failure(failure)
        print('\n\n')

        logger.exception(failure.err)

        return Engine.ResultType.NotFinished

    def on_exit(self) -> None:
        """ Quiting from Engine """
        for err in tuple(self.failures):
            if not err.critical:
                self.failures.remove(err)

        try:
            App.graphic.__release__()
        except AttributeError as exc:
            logger.error(f"can`t release graphic System, {exc.args[0]}")
        Engine.pg.quit()

        print()
        logger.success('ENGINE - QUIT\n')

    """ Main mainloop """

    @classmethod
    def mainloop(cls) -> None:
        """ mainloop of App (pre-, just, post- initializations and instance mainloop)
        Handle failures and show exception window """
        logger.info(
            f"Start Engine, "
            f"name: {Engine.data.MainData.APPLICATION_name}, "
            f"version: {Engine.data.MainData.APPLICATION_version} "
            f"at {'release' if Engine.data.MainData.IS_RELEASE else 'debug'} mode"
        )

        while App.running:
            logger.info("mainloop iteration\n")

            with Engine.failures.Catch(identifier=f"{App.mainloop}_Catch__ENGINE__") as c:
                data: Engine.assets.ConfigData = cls.__pre_init__()
                logger.success('ENGINE - PRE-INIT\n')
                cls(data)
                App.instance.run()

            if KeyboardInterrupt in c.failures:
                logger.info("KeyboardInterrupt - exit engine")
                return

            if App.instance:
                App.instance.on_exit()
            if App.instance.failures:
                # show err window
                App.running = err_screen.show_window() if Engine.data.MainData.IS_RELEASE \
                    else err_screen.show_window()
                App.instance.failures.clear()

            App.instance = None
