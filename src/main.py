# Third-party Imports
import pygame_menu

# Local Imports
import arcanoid.neat_evolution as neat
from base import BaseGame as bg
from base import game_menu
from arcanoid.arcanoid import Arcanoid


def main_menu():
    arcanoid = Arcanoid("Arcanoid", neat.main)

    main_menu = pygame_menu.Menu(
        title="Main Menu",
        width=bg.WIDTH,
        height=bg.HEIGHT,
        theme=bg.DARK_MODE,
    )

    main_menu._theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER

    main_menu.add.button(
        title="Arcanoid",
        action=game_menu(arcanoid),
        font_color=bg.WHITE,
        font_name=bg.ASSETS_PATH + "pixel_font.ttf",
        background_color=bg.BLACK,
    )

    main_menu.add.label(title="")

    main_menu.add.button(
        title="Exit",
        action=pygame_menu.events.EXIT,
        font_color=bg.WHITE,
        font_name=bg.ASSETS_PATH + "pixel_font.ttf",
        background_color=bg.BLACK,
    )

    main_menu.mainloop(arcanoid.screen)


if __name__ == "__main__":
    main_menu()
