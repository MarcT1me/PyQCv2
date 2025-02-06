import Engine


class Clip:
    def __init__(self, filename: str):
        self.sound = Engine.pg.mixer.Sound(filename)
        self.duration = self.sound.get_length()
        self.num_channels = self.sound.get_num_channels()
        self.raw = self.sound.get_raw()
        self.fadeout = 0

    @property
    def volume(self):
        return self.sound.get_volume()

    def play(
            self,
            loops: int = 0,
            maxtime: int = 0,
            fade_ms: int = 0
    ) -> None:
        self.sound.play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)

    def stop(self) -> None:
        self.sound.stop()

    def set_fadeout(self, milliseconds: int) -> None:
        self.fadeout = milliseconds
        self.sound.fadeout(milliseconds)
