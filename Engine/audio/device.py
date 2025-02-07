from loguru import logger

import Engine


class Device:
    def __init__(
            self,
            sys: 'Engine.audio.System', which: int, is_input,
            name: str, frequency=44100, channels=2, buffer=4096
    ):
        self._system = sys
        self.which = which
        self.is_input = is_input

        self.name = name
        self.params = (frequency, -16, channels, buffer)
        self.is_active = False
        self._channels = []

        logger.info(
            f"Engine audio Device - init ({'input' if is_input else 'output'})\n"
            f"index: {which},\n"
            f"is input: {is_input},\n"
            f"name: {name},\n"
            f"frequency: {frequency},\n"
            f"channels: {channels},\n"
            f"buffer: {buffer}"
        )

    @property
    def just(self):
        return self.new_channel()

    def activate(self):
        if self.is_active: return

        # Инициализируем микшер pygame для этого устройства
        Engine.pg.mixer.init(
            devicename=self.name,
            frequency=self.params[0],
            size=self.params[1],
            channels=self.params[2],
            buffer=self.params[3]
        )

        self.is_active = True

        logger.success(f"Engine audio Device - activate ({self.name})\n")

    def deactivate(self):
        """Деактивирует аудиоустройство"""
        self.stop_all()
        self.is_active = False

        logger.success(f"Engine audio Device - deactivate ({self.name})")

    def new_channel(self) -> 'Engine.audio.Channel':
        """Создает новый аудиоканал"""
        if not self.is_active:
            raise RuntimeError("Device is not active")

        ch = Engine.audio.Channel(device=self)
        self._channels.append(ch)
        return ch

    def stop_all(self):
        """Останавливает все каналы устройства"""
        for ch in self._channels:
            ch.stop()

    def __repr__(self):
        return f"<AudiDevice: {self.name} ({'active' if self.is_active else 'deactiva'})>"
