import Engine


class Device:
    def __init__(self, name: str, frequency=44100, channels=2, buffer=4096):
        self.name = name
        self.params = (frequency, -16, channels, buffer)
        self.is_active = False
        self._channels = []
        self._system = Engine.audio.System()

    def activate(self):
        if self.is_active: return

        # Инициализируем микшер pygame для этого устройства
        Engine.pg.mixer.quit()
        Engine.pg.mixer.init(
            devicename=self.name,
            frequency=self.params[0],
            size=self.params[1],
            channels=self.params[2],
            buffer=self.params[3]
        )

        self._system.set_active_device(self.name)
        self.is_active = True

    def deactivate(self):
        """Деактивирует аудиоустройство"""
        if not self.is_active:
            return

        self.stop_all()
        Engine.pg.mixer.quit()
        self.is_active = False

        if self._system.active_device == self:
            self._system._active_device = None

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
        return f"<AudiDevice: {self.name} ({'active' if self.is_active else 'inactive'})>"