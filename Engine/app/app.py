""" Collection of utilities for working with the application class.
"""
# default
from typing import TYPE_CHECKING, Type, final, Optional, cast
from abc import abstractmethod, ABC
...

# installed
from loguru import logger
...

# Engine import
import Engine
from Engine.app import err_screen
from Engine.app.app_data import AppData
from Engine.failures import IFailureHandler, Failure

# Engine interfaces
from Engine.objects.iinitanle import IPreInitable, IPostInitable
from Engine.objects.ieventful import IEventful
from Engine.objects.iupdatable import IPreUpdatable, IUpdatable
from Engine.objects.irenderable import IPreRenderable, IRenderable


class AppException(Exception):
    pass


class AppMainloopException(AppException):
    pass


class AppInitException(AppMainloopException):
    pass


class AppRunException(AppMainloopException):
    pass


class App(ABC, Engine.data.MetaObject,
          IPreInitable, IPostInitable,
          IEventful, IPreUpdatable, IUpdatable, IPreRenderable, IRenderable,
          IFailureHandler):
    """
    Main App class.
    The main parent class for creating logic and running it in the main loop
    
     METHODS:
      Initializations:
       1) pre-init - Thr method for loading assets and initializing data for further program initialization
       2) win-data - The method that is called during initialization to create a window data class
       3) gl-data - The method called after creating the window data is needed to create graphics data
       4) post-init - a method for processing some data after initialization, for example, for calling third-party programs or launching the download interface
      Mainloop:
       5) events -: Event handling method
       6) pre-update - A preliminary update of the application data. Sometimes it is necessary before the `update`
       7) update - The main update of the program data
       8) pre-render - Pre-rendering of surfaces. It is used for pre-renders and data transfer to the shader.
       9) render - Rendering the program window
      Lunching:
       10) run - The main cycle of the program
       11) mainloop - the main running method of the program

     CLASS FIELDS:
      * running (bool) - a variable is a condition for the operation of the main loop
      * inherited - A Inherited App class
      * instance - A current app instance

      Systems:
       * assets - for loading assets,
       * clock - timing system for controlling cycle tile,
       * audio - for playing sounds,
       * event - for handling events and creating user Event classes,
       * graphic - The graphic system for controlling Window and GL objects

      Also:
       * all AppData fields
    """
    """ AppData object """
    data: AppData
    # AppData
    fps: int  # clock
    data_table: Engine.data.arrays.DataTable  # data
    assets_type_configs: list[Engine.assets.AssetLoader]  # assets
    failures: list[Failure]  # Error catching
    joysticks: dict[int, Engine.pg.joystick.JoystickType]  # joysticks
    root_scene_object_id: Engine.data.Identifier  # Scene and space context

    """ The App class object Data """
    running: bool = True  # in App.running - Engine loop, in self.running - App loop
    # inherited app class and current app instance
    inherited: 'Type[App]' = cast('Type[App]', None)
    instance: 'App' = cast('App', None)

    """ Engine Systems """
    # pre-init
    assets: Engine.assets.AssetManager = None
    # init
    clock: Engine.timing.TimingSystem = None
    audio: Engine.audio.AudioSystem = None
    event: Engine.events.EventSystem = None
    graphic: Engine.graphic.GraphicSystem = None

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

    def __repr__(self) -> str:
        return f'<App: {Engine.data.MainData.APPLICATION_name} (running={self.running})>'

    """ __pre_init__ logic """

    def __new__(cls, *args, **kwargs):
        Engine.pg.init()
        App.instance = super().__new__(cls)
        return App.instance

    @abstractmethod
    def __pre_init__(self) -> AppData:
        """ App pre-initialisation.
        After lunching (inherited App.mainloop()).
        Before main __init__ logic.
        Using for init AppData and for initialization Asset Manager. """

    @staticmethod
    @final
    def init_asset_manager(*asset_loaders: Optional[list[Engine.assets.AssetLoader]]) -> None:
        """ Initialize Asset manager.
        Need to use in __pre_init__.
        1) adding default assets loaders
        2) AssetManager.__init__ """
        asset_loaders = list(asset_loaders)
        asset_loaders.extend([
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
            # Texture Asset
            Engine.assets.texture.TextureAssetLoader(
                Engine.assets.AssetType(Engine.DataType.PyGame | Engine.DataType.Texture)
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
        App.assets = Engine.assets.AssetManager(asset_loaders)

    """ Main __init__ logic """

    @abstractmethod
    def __win_data__(self) -> Engine.graphic.WinData:
        """ Pre-initialisation -> Initialization main Window Data.
        After inherited __pre_init__ but in App.__init__ -> Engine.graphic.System.__init__ """

    @staticmethod
    def __gl_data__(win_data: Engine.graphic.WinData) -> Engine.graphic.GL.GlData:
        """ Pre-initialisation -> Initialization Graphic Libreary Data.
        After __win_data__
        Take WinData from the __win_data__"""
        return Engine.graphic.GL.GlData(win_data=win_data) if Engine.data.MainData.IS_USE_GL else None

    @abstractmethod
    def __init__(self) -> None:
        """ Engine Initialization -> Initialization systems.
        Before inherited __pre_init__.
        Take AppData from the __pre_init__ """
        super().__init__(self.__pre_init__())
        logger.success('ENGINE - PRE-INIT\n')
        # init systems
        App.clock = Engine.timing.TimingSystem(self.data.fps)
        App.audio = Engine.audio.AudioSystem()
        App.graphic = Engine.graphic.GraphicSystem()
        App.event = Engine.events.EventSystem()

        logger.success('ENGINE - INIT\n')

    """ App instance mainloop logic """

    def __post_init__(self) -> None:
        """ Engine post-initialisation.
        Before inherited __init__
        Calling in instance App.mainloop"""
        App.graphic.__post_init__()
        logger.success("ENGINE - POST-INIT\n")

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
        @abstractmethod
        def render(self) -> None:
            """ render all app surfaces, and use engine render methods """
            ...
    else:
        @abstractmethod
        def render(self) -> None:
            """ render all app surfaces, and use engine render methods """
            ...

    """ App exit logic """

    @staticmethod
    def critical_failure(err):
        """ Using when app catch critical failure
        Already Implement in App.on_failure """
        App.instance.failures.append(err)
        App.running = False

    def on_failure(self, failure: Failure) -> None:
        """ Calling when Ap got exception in mainloop """
        if isinstance(failure.err, KeyboardInterrupt):
            return Engine.ResultType.Finished

        if failure.critical:
            App.critical_failure(failure)
        print('\n\n')

        logger.exception(failure)

        return Engine.ResultType.NotFinished

    def on_exit(self) -> None:
        """ Quiting from Engine """
        for err in tuple(self.failures):
            if not err.critical:
                self.failures.remove(err)

        try:
            App.graphic.release()
        except AttributeError as exc:
            logger.error(f"can`t release graphic System, {exc.args[0]}")
        Engine.pg.quit()

        print()
        logger.success('ENGINE - QUIT\n')

    """ Main mainloop """

    # running app
    @final
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
            self.events()
            Engine.threading.EventThread.wait()

            # update
            self.pre_update()
            Engine.threading.PreUpdateThread.wait()

            self.update()
            Engine.threading.UpdateThread.wait()

            # render
            self.pre_render()
            Engine.threading.PreRenderThread.wait()

            self.graphic.prepare()
            self.render()
            self.graphic.flip()
            # clok tick
            App.clock.tick()

    @classmethod
    @final
    def mainloop(cls) -> None:
        """ mainloop of App (pre-, just, post- initializations and instance mainloop)
        Handle failures and show exception window """
        logger.info(
            f"Start Engine, "
            f"name: {Engine.data.MainData.APPLICATION_name}, "
            f"version: {Engine.data.MainData.APPLICATION_version} "
            f"at {'release' if Engine.data.MainData.IS_RELEASE else 'debug'} mode"
        )

        def exiting():
            # exiting
            try:
                if App.instance:
                    App.instance.on_exit()

            except Exception as e:
                raise AppMainloopException("Instance is not created") from e

        def handle_critical_errors():
            # show err window
            if App.instance:
                App.running = err_screen.show_window(App.instance.data.failures) if Engine.data.MainData.IS_RELEASE \
                    else err_screen.show_window(App.instance.data.failures)
                App.instance.failures.clear()
            else:
                logger.error("Cant use App.instance, exiting from app")
                App.running = False
                err_screen.show_window(
                    [AppMainloopException("Cant use default error handling")],
                    restartale=False
                )

        class MainloopHandler(IFailureHandler):
            def on_failure(self, failure: Failure) -> None:
                if isinstance(failure.err, KeyboardInterrupt):
                    logger.warning("KeyboardInterrupt - exit engine")
                    App.running = False
                    return

                logger.exception(failure)

                handle_critical_errors()

        handler = MainloopHandler()

        with Engine.failures.Catch(identifier=f"{App.mainloop} Catch__ENGINE__", handler=handler) as cth:
            while App.running:
                logger.info("mainloop iteration\n")

                instance = cth.try_func(cls)

                cth.try_func(instance.run)

                exiting()

                if instance.failures:
                    handle_critical_errors()

                App.instance = None
