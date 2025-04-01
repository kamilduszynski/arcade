# Standard Library Imports
import os
import sys
from collections.abc import Callable

# Third-party Imports
import pygame
import pygame_menu

# Local Imports
from tools.utils import key_down, get_repo_path


class BaseGame:
    repo_path = get_repo_path()

    ASSETS_PATH = os.path.join(repo_path, "assets/")
    CONFIGS_PATH = os.path.join(repo_path, "configs/")
    MODEL_PATH = os.path.join(repo_path, "models/best_genome.pickle")
    CHECKPOINT_PATH = os.path.join(repo_path, "models/neat-checkpoint-")

    WIDTH = 600
    HEIGHT = 400
    ROW_NUMBER = 4
    COLUMN_NUMBER = 10
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    DARK_MODE = pygame_menu.themes.THEME_DARK.copy()
    DARK_MODE.background_color = BLACK

    def __init__(self, game_name: str, simulation: Callable):
        pygame.init()
        pygame.display.set_caption(game_name)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        self.game_name = game_name
        self.simulation = simulation
        self.score = 0
        self.text_font = pygame.font.Font(BaseGame.ASSETS_PATH + "pixel_font.ttf", 15)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, BaseGame.HEIGHT))

    def main(self):
        pass

    def game_over(self):
        game_over_font = pygame.font.Font(BaseGame.ASSETS_PATH + "pixel_font.ttf", 50)
        game_over_score_font = pygame.font.Font(
            BaseGame.ASSETS_PATH + "pixel_font.ttf", 35
        )

        while True:
            self.screen.fill(BaseGame.BLACK)
            game_over_text = game_over_font.render("Game over", 1, BaseGame.WHITE)
            self.screen.blit(game_over_text, (160, 80))
            game_over_text = game_over_score_font.render(
                f"Score: {self.score}", 1, BaseGame.WHITE
            )
            self.screen.blit(game_over_text, (240, 150))
            restart_text = self.text_font.render(
                "Press space to play again", 1, BaseGame.WHITE
            )
            self.screen.blit(restart_text, (200, 240))
            restart_text = self.text_font.render(
                "Press enter to go back to game menu", 1, BaseGame.WHITE
            )
            self.screen.blit(restart_text, (150, 300))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif key_down("ESCAPE"):
                    pygame.quit()
                    sys.exit()
                elif key_down("SPACE"):
                    self.main()
                elif key_down("RETURN"):
                    menu = game_menu(self)
                    menu.mainloop(self.screen)
            pygame.display.update()


def game_menu(game):
    game_menu = pygame_menu.Menu(
        title=f"{game.game_name.capitalize()} Menu",
        width=BaseGame.WIDTH,
        height=BaseGame.HEIGHT,
        theme=BaseGame.DARK_MODE,
    )

    game_menu._theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER

    game_menu.add.button(
        title="Play game",
        action=game.main,
        font_color=BaseGame.WHITE,
        font_name=BaseGame.ASSETS_PATH + "pixel_font.ttf",
        background_color=BaseGame.BLACK,
    )

    game_menu.add.label(title="")

    game_menu.add.button(
        title="Run simulation",
        action=game.simulation,
        font_color=BaseGame.WHITE,
        font_name=BaseGame.ASSETS_PATH + "pixel_font.ttf",
        background_color=BaseGame.BLACK,
    )

    game_menu.add.label(title="")
    return game_menu
