import time
import pygame


class Button:
    roster = dict()

    def __init__(self, _id: str, *,
                 # WINDOW
                 size: tuple[int, int] = (100, 100),
                 pos: tuple[int, int] = (0, 0),
                 source: str = None,
                 image_pos: tuple = (0, 0),
                 # TEXT
                 text: str = '',
                 text_size: int = 20,
                 text_pos: tuple = (0, 0),
                 text_center: bool = False,
                 text_clor: tuple[int, int, int] = (220, 220, 220),
                 text_bold: bool = True,
                 # COLORS
                 font: str = 'Arial',
                 bgcolor_on_press: tuple[int, int, int] = (100, 150, 250),
                 bgcolor_not_press: tuple[int, int, int] = (120, 120, 120),
                 # FUNCTIONAL
                 on_press=lambda: None,
                 on_clamping=lambda: None,
                 on_release=lambda: None,
                 release_long: float = 1
                 ) -> None:
        """ INIT a button class and assigning values. """
        self.id = _id
        """ RECT """
        self.pos: tuple = pos
        self.size: tuple = size

        """ IMAGE """
        self.image = pygame.transform.scale(pygame.image.load(source), size) if source is not None else None
        self.image_pos = image_pos

        """ TEXT """
        self.text: str = text
        self.text_size: int = text_size
        self.text_clor: tuple = text_clor
        self.font = pygame.font.SysFont(font, self.text_size, bold=text_bold).render(self.text, True, self.text_clor)
        self.font_size: tuple = self.font.get_size()
        self.text_pos: tuple = (
            text_pos[0] - self.font.get_width() // 2, text_pos[1] - self.font.get_height() // 2
        ) if text_center else text_pos

        """ SURFACE """
        self.surf = pygame.Surface(size)
        self.bgcolor_on_press: tuple = bgcolor_on_press
        self.bgcolor_not_press: tuple = bgcolor_not_press
        self.surf_color: tuple = bgcolor_not_press
        self.surf.set_colorkey(self.surf_color) if self.image is not None else Ellipsis

        """ FUNCTION """
        self.release_start = None
        self.release_long = release_long

        self.on_press = on_press
        self.on_clamping = on_clamping
        self.on_release = on_release
        self.roster[_id] = self

    def __event__(self, event: pygame.event.Event) -> None:
        """ События кнопки, нажатие (короткое/долгое) и реализация функционала """
        if self.release_start is not None:
            if self.release_start + self.release_long <= time.time():
                """ Долгое удержание """
                self.on_clamping()  # долгое нажатие

                self.release_start = None  # сброс значений нажатия
                return

        if event.type == pygame.MOUSEBUTTONDOWN:
            """ Нажатие """
            if pygame.rect.Rect(*self.pos, *self.size).collidepoint(pygame.mouse.get_pos()):
                # изменение цвета на активное
                self.surf_color = self.bgcolor_not_press if self.image is not None else self.bgcolor_on_press

                if self.release_start is None:  # ставлю значение нажатия
                    self.release_start = time.time()

            else:
                self.surf_color = self.bgcolor_not_press

        elif event.type == pygame.MOUSEBUTTONUP:
            """ Отжатие """
            self.surf_color = self.bgcolor_not_press  # изменение цвета на не активное

            if self.release_start is not None:
                if self.release_start + self.release_long >= time.time():
                    """ Недолгое удержание """
                    self.on_press()  # недолгое нажатие

                self.release_start = None  # сброс значений нажатия

    def __render__(self, win) -> None:
        """ Render button """
        self.surf.fill(self.surf_color)

        self.surf.blit(self.image, self.image_pos) if self.image is not None else Ellipsis
        self.surf.blit(self.font, self.text_pos)  # отображение текста и изображения кнопки

        win.blit(self.surf, self.pos)

    def release(self):
        self.roster.pop(self.id)

    @staticmethod
    def roster_event(event):
        for btn in Button.roster.values():
            btn.__event__(event)

    @staticmethod
    def roster_render(win):
        for btn in Button.roster.values():
            btn.__render__(win)

    @staticmethod
    def roster_relies():
        for btn in list(Button.roster.values()):
            btn.release()
