import traceback

from Engine import pg as pygame
from Engine.data import FileSystem
from Engine.scripts.button import Button


def show_window(*,
                caption: str = 'Error Message', custom_surf: pygame.Surface | str = None, flags: int = pygame.NOFRAME
                ) -> bool:
    """ processing error """
    from Engine.app import App
    pygame.quit()
    pygame.init()

    custom_surf, custom_surf_arg = pygame.Surface((270, 110)), custom_surf
    custom_surf.fill((0, 255, 0))
    if custom_surf_arg == 'base':
        custom_surf.blit(
            pygame.font.SysFont('Verdana', 35, bold=True).render(
                'Gravity', False, 'black'
            ),
            (7, 0)
        )
        custom_surf.blit(
            pygame.font.SysFont('Verdana', 35, bold=True).render(
                'Simulation', False, 'black'
            ),
            (50, 51)
        )
    if custom_surf_arg != 'fill':
        custom_surf.set_colorkey((0, 255, 0)) if custom_surf is not None else Ellipsis

    """ Working with pygame """
    clock = pygame.time.Clock()
    # process background
    background = pygame.image.load(rf'{FileSystem.__ENGINE_DATA__}\presets/messages/err_background.png')
    background = pygame.transform.scale_by(background, .75)
    # screen
    screen_size = background.get_size()
    screen = pygame.display.set_mode(screen_size, flags=flags)
    white_surf = pygame.Surface(screen_size)
    white_surf.fill('white')
    pygame.display.set_icon(
        pygame.image.load(
            rf'{FileSystem.__ENGINE_DATA__}\presets\Service.png'
        )
    )
    # caption
    pygame.display.set_caption(str(caption))

    def exit_func(res):
        nonlocal result, running
        result, running = res, False

    """ fonts and other graphic """

    def restart_btn():
        exit_func(True)

    def exit_btn():
        exit_func(False)

    btn1 = Button('1',
                  size=(302, 40), pos=(10, screen_size[1] - 50),
                  text='Restart', font='Unispace', text_size=45, text_bold=False,
                  bgcolor_on_press=(150, 150, 150),
                  text_pos=(151, 20), text_center=True,
                  on_press=restart_btn
                  )
    Button('2',
           size=(302, 40), pos=(btn1.size[0] + 30, btn1.pos[1]),
           text='Exit', font='Unispace', text_size=45, text_bold=False,
           bgcolor_not_press=(255, 50, 50), bgcolor_on_press=(255, 120, 120),
           text_center=True, text_pos=(151, 20),
           on_press=exit_btn
           )
    font_color = (50, 50, 50)
    err_text_font = pygame.font.SysFont('Unispace', 30).render(
        f'text: `{[err.err for err in App.failures]}`', True, font_color
    )
    err_type_font = pygame.font.SysFont('Unispace', 30).render(
        f'type: {[str(type(err.err))[8:-2] for err in App.failures]}', True, font_color
    )
    help_font = pygame.font.SysFont('Unispace', 30).render(
        "press on 'BUTTON' or 'R' to restart and 'BUTTON', 'Esc' or 'QUIT'", True, (20, 20, 20)
    )

    result: bool = False
    running: bool = True
    while running:
        """err while"""

        """ events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_func(False)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_func(False)
                elif event.key == pygame.K_r:
                    exit_func(True)
            Button.roster_event(event)

        """ render """
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(err_text_font, (screen_size[0] - err_text_font.get_width() - 30, 20))
        screen.blit(err_type_font, (130, 300))
        screen.blit(custom_surf, (780, 345))
        screen.blit(help_font, (12, 420))
        Button.roster_render(screen)

        """ __PyGame__ """
        pygame.display.flip(), clock.tick(60)
    pygame.quit()
    Button.roster_relies()
    return result


if __name__ == '__main__':
    try:
        try:
            raise UnicodeDecodeError('UTF-8', b'\\', 0, 0, 'err')
        except Exception as exc:
            print(show_window(custom_surf='base'))
    except Exception as exc:
        traceback.print_exception(exc)
        input()
