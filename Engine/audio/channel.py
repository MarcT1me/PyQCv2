from typing import Optional, Iterable, Self
from loguru import logger

import Engine


class Channel:
    i = 0

    def __init__(self, device: 'Engine.audio.Device'):
        self.device = device

        self.channel = Engine.pg.mixer.Channel(Channel.i)
        Channel.i += 1
        self.current_clip: Optional[Engine.audio.Clip] = None

        self.paused = False
        self.start_time = 0
        self.pause_position = 0

        self.fadeout = 0

    @property
    def endevent(self):
        return self.channel.get_endevent()

    @endevent.setter
    def endevent(self, value: Engine.events.Event):
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
    ) -> Self:
        if not isinstance(clip, Engine.audio.Clip):
            logger.warning("cant play given clip")
            return

        self._check_active()

        self.stop()
        self.current_clip = clip
        self.start_time = Engine.timing.uix_time() - start_time
        self.channel.play(clip.sound, loops=loops, maxtime=maxtime, fade_ms=fade_ms)

        if start_time > 0:
            self.set_position(start_time)

        return self

    def stop(self) -> Self:

        self.channel.stop()
        self.current_clip = None
        self.paused = False
        self.pause_position = 0

        return self

    def pause(self) -> Self:
        """Приостановка воспроизведения"""
        self._check_active()

        if self.is_playing() and not self.paused:
            self.pause_position = self.get_position()
            self.channel.pause()
            self.paused = True

        return self

    def resume(self) -> Self:
        """Продолжение воспроизведения с места паузы"""
        self._check_active()

        if self.paused and self.current_clip:
            self.play(self.current_clip, self.pause_position)
            self.paused = False

        return self

    @property
    def volume(self) -> float | tuple[float, float]:
        return self.channel.get_volume()

    @volume.setter
    def volume(self, volume=float | tuple[float, float]) -> None:
        """Установка стерео громкости"""
        self._check_active()
        self.set_volume(*volume if isinstance(volume, Iterable) else volume)

    def set_volume(self, left: float, right: Optional[float] = None) -> Self:
        """Установка стерео громкости"""
        self._check_active()

        if right is None:
            right = left
        self.channel.set_volume(left, right)

        return self

    @property
    def position(self) -> float:
        return self.get_position()

    @position.setter
    def position(self, item: float) -> None:
        self.set_position(item)

    def get_position(self) -> float:
        """Текущая позиция воспроизведения в секундах"""
        if self.paused:
            return self.pause_position

        if self.is_playing():
            return Engine.timing.uix_time() - self.start_time
        return 0.0

    def set_position(self, seconds: float) -> Self:
        self._check_active()

        if self.current_clip:
            seconds = max(0, min(seconds, self.current_clip.duration))
            if self.is_playing():
                self.stop()
            self.play(self.current_clip, seconds)

        return self

    def is_playing(self) -> bool:
        return self.channel.get_busy() and not self.paused

    def wait_playing(self) -> None:
        while self.is_playing():
            Engine.timing.System.wait(100)

    def set_fadeout(self, milliseconds: int) -> Self:
        self.fadeout = milliseconds
        self._check_active()
        self.channel.fadeout(milliseconds)

        return self
