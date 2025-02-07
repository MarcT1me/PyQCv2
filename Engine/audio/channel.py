from typing import Optional

import Engine


class Channel:
    def __init__(self, device: 'Engine.audio.Device'):
        self.device = device

        self.channel = Engine.pg.mixer.Channel(Engine.pg.mixer.get_num_channels())
        self.current_clip: Optional[Engine.audio.Clip] = None

        self.paused = False
        self.start_time = 0
        self.pause_position = 0

        self.fadeout = 0

    @property
    def volume(self):
        return self.channel.get_volume()

    @property
    def endevent(self):
        return self.channel.get_endevent()

    @endevent.setter
    def endevent(self, value: 'Engine.event.Event'):
        self.channel.set_volume(value.event)

    def _check_active(self) -> None:
        if not self.device.is_active:
            raise RuntimeError("Parent device is not active")

    def play(
            self,
            clip: 'Engine.audio.Clip',
            loops: int = 0,
            maxtime: int = 0,
            fade_ms: int = 0,
            start_time: float = 0.0
    ) -> None:
        self._check_active()

        self.stop()
        self.current_clip = clip
        self.start_time = Engine.timing.uix_time() - start_time
        self.channel.play(clip.sound, loops=loops, maxtime=maxtime, fade_ms=fade_ms)

        if start_time > 0:
            self.set_position(start_time)

    def stop(self) -> None:

        self.channel.stop()
        self.current_clip = None
        self.paused = False
        self.pause_position = 0

    def pause(self) -> None:
        """Приостановка воспроизведения"""
        self._check_active()

        if self.is_playing() and not self.paused:
            self.pause_position = self.get_position()
            self.channel.pause()
            self.paused = True

    def resume(self) -> None:
        """Продолжение воспроизведения с места паузы"""
        self._check_active()

        if self.paused and self.current_clip:
            self.play(self.current_clip, self.pause_position)
            self.paused = False

    def set_volume(self, left: float, right: Optional[float] = None) -> None:
        """Установка стерео громкости"""
        self._check_active()

        if right is None:
            right = left
        self.channel.set_volume(left, right)

    def get_position(self) -> float:
        """Текущая позиция воспроизведения в секундах"""
        if self.paused:
            return self.pause_position

        if self.is_playing():
            return Engine.timing.uix_time() - self.start_time
        return 0.0

    def set_position(self, seconds: float) -> None:
        self._check_active()

        if self.current_clip:
            seconds = max(0, min(seconds, self.current_clip.duration))
            if self.is_playing():
                self.stop()
            self.play(self.current_clip, seconds)

    def is_playing(self) -> bool:
        return self.channel.get_busy() and not self.paused

    def wait_playing(self) -> None:
        while self.is_playing():
            Engine.timing.System.wait(100)

    def set_fadeout(self, milliseconds: int) -> None:
        self.fadeout = milliseconds
        self._check_active()
        self.channel.fadeout(milliseconds)
