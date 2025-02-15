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
            self.handle_default(self, event=event)

        logger.success("Engine event System - init\n")

    def prepare(self):
        self.event_list = Engine.pg.event.get()
        self.key_list = Engine.pg.key.get_pressed()

    @Engine.decorators.with_store(already_handled=False)
    @Engine.decorators.window_event(already_single=True)
    def handle_default(self, *, event: Engine.pg.event.Event, window: int | None):
        """ Engine default event handling """
        if self.handle_default.already_handled:
            self.handle_default.already_handled = False
            return

        if event.type == Engine.pg.QUIT:
            Engine.App.running = False
        elif event.type == Engine.pg.WINDOWRESIZED:
            if window:
                ...
            else:
                Engine.App.graphic.window.data.extern({"size": Engine.math.vec2(event.x, event.y)})
                Engine.App.WorkingInstance.events.defer(Engine.App.graphic.resset)
        elif event.type == Engine.pg.WINDOWMOVED:
            if window:
                ...
        elif event.type == Engine.pg.WINDOWDISPLAYCHANGED:
            if window:
                ...
            else:
                Engine.App.graphic.window.data.extern({"monitor": event.display_index})
        elif event.type == Engine.pg.JOYDEVICEADDED:
            joy = Engine.pg.joystick.Joystick(event.device_index)
            Engine.App.joysticks[joy.get_instance_id()] = joy
        elif event.type == Engine.pg.JOYDEVICEREMOVED:
            del Engine.App.joysticks[event.instance_id]
        elif event.type == Engine.pg.AUDIODEVICEADDED:
            Engine.App.audio.add_device(event.which, bool(event.iscapture))
        elif event.type == Engine.pg.AUDIODEVICEREMOVED:
            Engine.App.audio.remove_device(event.which, bool(event.iscapture))
        elif event.type == Engine.audio.System.update_default.event.type:
            if event.is_input | 1:
                Engine.App.audio.set_default_device(False)
            if event.is_input | 2:
                Engine.App.audio.set_default_device(True)
