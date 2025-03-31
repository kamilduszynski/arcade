# Third-party Imports
import pygame_menu

# Local Imports
import arcanoid.arcanoid as arc
import arcanoid.neat_evolution as neat


def main_menu():
    dark_mode_theme = pygame_menu.themes.THEME_DARK.copy()
    dark_mode_theme.background_color = arc.Arcanoid.BLACK

    game = arc.Arcanoid("Arcanoid")

    main_menu = pygame_menu.Menu(
        title="Main Menu",
        width=arc.Arcanoid.WIDTH,
        height=arc.Arcanoid.HEIGHT,
        theme=dark_mode_theme,
    )

    main_menu._theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER

    main_menu.add.button(
        title="Play game",
        font_color=arc.Arcanoid.WHITE,
        font_name=arc.Arcanoid.ASSETS_PATH + "pixel_font.ttf",
        background_color=arc.Arcanoid.BLACK,
        accept_kwargs=True,
        action=game.main,
    )

    main_menu.add.label(title="")

    main_menu.add.button(
        title="Run simulation",
        action=neat.main,
        font_color=arc.Arcanoid.WHITE,
        font_name=arc.Arcanoid.ASSETS_PATH + "pixel_font.ttf",
        background_color=arc.Arcanoid.BLACK,
    )

    main_menu.add.label(title="")

    main_menu.add.button(
        title="Exit",
        action=pygame_menu.events.EXIT,
        font_color=arc.Arcanoid.WHITE,
        font_name=arc.Arcanoid.ASSETS_PATH + "pixel_font.ttf",
        background_color=arc.Arcanoid.BLACK,
    )

    main_menu.mainloop(game.screen)


if __name__ == "__main__":
    main_menu()
