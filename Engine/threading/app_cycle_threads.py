from typing import final, Self
from loguru import logger

import Engine
from Engine.threading.thread import Thread, ThreadRoster


@final
class EventThread(Thread, Engine.failures.IFailureHandler):
    """ Thread class for Handling GUI Events """

    _roster: ThreadRoster[str, Self] = ThreadRoster()

    def on_failure(self, err: Engine.failures.Failure):
        logger.error("Failure catching from EventThread")
        Engine.App.instance.on_failure(err)


@final
class PreUpdateThread(Thread, Engine.failures.IFailureHandler):
    """ Thread class for pre updating app """

    _roster: ThreadRoster[str, Self] = ThreadRoster()

    def on_failure(self, err: Engine.failures.Failure):
        logger.error("Failure catching from PreUpdateThread")
        Engine.App.instance.on_failure(err)


@final
class UpdateThread(Thread, Engine.failures.IFailureHandler):
    """ Thread class for updating app """

    _roster: ThreadRoster[str, Self] = ThreadRoster()

    def on_failure(self, err: Engine.failures.Failure):
        logger.error("Failure catching from UpdateThread")
        Engine.App.instance.on_failure(err)


@final
class PreRenderThread(Thread, Engine.failures.IFailureHandler):
    """ Thread class for pre rendering app """

    _roster: ThreadRoster[str, Self] = ThreadRoster()

    def on_failure(self, err: Engine.failures.Failure):
        logger.error("Failure catching from PreRenderThread")
        Engine.App.instance.on_failure(err)
