# Third-party Imports
import pygame_menu

# Local Imports
import arcanoid
import neat_evolution


def main_menu():
    dark_mode_theme = pygame_menu.themes.THEME_DARK.copy()
    dark_mode_theme.background_color = arcanoid.BLACK

    text_font, clock, screen = arcanoid.game_init()

    main_menu = pygame_menu.Menu(
        title="Main Menu",
        width=arcanoid.WIDTH,
        height=arcanoid.HEIGHT,
        theme=dark_mode_theme,
    )

    main_menu._theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER

    main_menu.add.button(
        title="Play game",
        font_color=arcanoid.WHITE,
        font_name=arcanoid.ASSETS_PATH + "pixel_font.ttf",
        background_color=arcanoid.BLACK,
        accept_kwargs=True,
        action=arcanoid.main,
        text_font=text_font,
        clock=clock,
        screen=screen,
    )

    main_menu.add.label(title="")

    main_menu.add.button(
        title="Run simulation",
        action=neat_evolution.main,
        font_color=arcanoid.WHITE,
        font_name=arcanoid.ASSETS_PATH + "pixel_font.ttf",
        background_color=arcanoid.BLACK,
    )

    main_menu.add.label(title="")

    main_menu.add.button(
        title="Exit",
        action=pygame_menu.events.EXIT,
        font_color=arcanoid.WHITE,
        font_name=arcanoid.ASSETS_PATH + "pixel_font.ttf",
        background_color=arcanoid.BLACK,
    )

    main_menu.mainloop(screen)


if __name__ == "__main__":
    main_menu()
