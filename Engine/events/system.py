from typing import final
from loguru import logger

import Engine


@final
class System:
    def __init__(self):
        self.event_list: list[Engine.pg.event.EventType] = []
        self.key_list: Engine.pg.key.ScancodeWrapper = []

        Engine.audio.System.update_default.post()
        self.prepare()

        for event in self.event_list:
            self.handle_default(event=event)

        logger.success("Engine event System - init\n")

    def prepare(self):
        self.event_list = Engine.pg.event.get()
        self.key_list = Engine.pg.key.get_pressed()

    @Engine.decorators.storage(already_handled=False)
    @Engine.decorators.window_event(already_single=True)
    def handle_default(self, *, event: Engine.pg.event.Event, window: int | None):
        """ Engine default event handling """
        if System.handle_default.already_handled:
            System.handle_default.already_handled = False
            return

        if event.type == Engine.pg.QUIT:
            Engine.App.running = False
        elif event.type == Engine.pg.WINDOWRESIZED:
            if window:
                ...
            else:
                Engine.App.inherited.events.defer(
                    Engine.App.graphic.window.data.modify, True,
                    size=Engine.math.vec2(event.x, event.y)
                )
                Engine.App.inherited.events.defer(
                    Engine.App.graphic.resset, True
                )
        elif event.type == Engine.pg.WINDOWMOVED:
            if window:
                ...
        elif event.type == Engine.pg.WINDOWDISPLAYCHANGED:
            if window:
                ...
            else:
                Engine.App.inherited.events.defer(
                    Engine.App.graphic.window.data.modify, True,
                    monitor=event.display_index
                )
                logger.info(f"Engine Window - change monitor: {event.display_index}\n")

        # coming soon
        elif event.type == Engine.pg.WINDOWMINIMIZED:
            logger.info(f"Engine Window - minimized: {window}\n")
        elif event.type == Engine.pg.WINDOWMAXIMIZED:
            logger.info(f"Engine Window - maximized: {window}\n")
        elif event.type == Engine.pg.WINDOWFOCUSGAINED:
            logger.info(f"Engine Window - take gained: {window}\n")
        elif event.type == Engine.pg.WINDOWFOCUSLOST:
            logger.info(f"Engine Window - lost focus: {window}\n")

        elif event.type == Engine.pg.JOYDEVICEADDED:
            joy = Engine.pg.joystick.Joystick(event.device_index)
            Engine.App.instance.data.joysticks[joy.get_instance_id()] = joy
            logger.info(f"PyGame Joystick - added: {event.device_index}\n")
        elif event.type == Engine.pg.JOYDEVICEREMOVED:
            del Engine.App.joysticks[event.instance_id]
            logger.info(f"PyGame Joystick - removed: {event.instance_id}\n")
        elif event.type == Engine.pg.AUDIODEVICEADDED:
            Engine.App.audio.add_device(event.which, bool(event.iscapture))
        elif event.type == Engine.pg.AUDIODEVICEREMOVED:
            Engine.App.audio.remove_device(event.which, bool(event.iscapture))
        elif event.type == Engine.audio.System.update_default.event.type:
            if event.is_input | 1:
                Engine.App.audio.set_default_device(False)
            if event.is_input | 2:
                Engine.App.audio.set_default_device(True)
