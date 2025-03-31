# Standard Library Imports
import os
import sys
from random import randint

# Third-party Imports
import pygame

# Local Imports
from main import main_menu
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

    def __init__(self, game_name: str):
        pygame.init()
        pygame.display.set_caption(game_name)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        self.score = 0
        self.text_font = pygame.font.Font(BaseGame.ASSETS_PATH + "pixel_font.ttf", 20)
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
            self.screen.blit(game_over_text, (210, 150))
            restart_text = self.text_font.render(
                "Press space to play again", 1, BaseGame.WHITE
            )
            self.screen.blit(restart_text, (160, 240))
            restart_text = self.text_font.render(
                "Press enter to go back to main menu", 1, BaseGame.WHITE
            )
            self.screen.blit(restart_text, (110, 300))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif key_down("ESCAPE"):
                    pygame.quit()
                    sys.exit()
                elif key_down("SPACE"):
                    self.main(self.text_font, self.clock, self.screen)
                elif key_down("RETURN"):
                    main_menu()
            pygame.display.update()


class Player:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = BaseGame.WIDTH / 6
        self.hight = 20
        self.velocity = 0
        asset = pygame.image.load(BaseGame.ASSETS_PATH + "player.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.hight))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x += self.velocity

    def move_right(self):
        self.velocity = 4
        self.move()

        if self.rect.x > (BaseGame.WIDTH - self.width):
            self.rect.x = BaseGame.WIDTH - self.width

    def move_left(self):
        self.velocity = -4
        self.move()

        if self.rect.x < 0:
            self.rect.x = 0


class Block:
    width = BaseGame.WIDTH / BaseGame.COLUMN_NUMBER
    height = 20

    def __init__(self, x: int, y: int, block_version: int) -> None:
        self.x = x
        self.y = y
        asset = pygame.image.load(
            BaseGame.ASSETS_PATH + f"block{block_version}.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.surface):
        screen.blit(self.image, self.rect)

    @staticmethod
    def spawn() -> list:
        blocks = []

        for i in range(BaseGame.ROW_NUMBER):
            for j in range(BaseGame.COLUMN_NUMBER):
                block = Block(
                    j * Block.width + Block.width / 2,
                    i * Block.height + Block.height / 2,
                    (j + i) % 4,
                )
                blocks.append(block)
        return blocks


class Ball:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.vertical_velocity = 3
        self.horizontal_velocity = randint(-3, 3)
        asset = pygame.image.load(BaseGame.ASSETS_PATH + "ball.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def move(self, player: Player, blocks: list[Block]):
        self.rect.x += self.horizontal_velocity
        self.rect.y += self.vertical_velocity

        if self.rect.x <= 0:
            self.rect.x = 0
            self.horizontal_velocity = -self.horizontal_velocity

        if self.rect.x > BaseGame.WIDTH - self.width:
            self.rect.x = BaseGame.WIDTH - self.width
            self.horizontal_velocity = -self.horizontal_velocity

        if self.rect.y <= 0:
            self.rect.y = 0
            self.vertical_velocity = -self.vertical_velocity

        if self.rect.y >= BaseGame.HEIGHT - self.height:
            return -1

        if self.rect.colliderect(player.rect):
            randomizer = randint(-10, 10) * 0.1
            self.horizontal_velocity += player.velocity + randomizer
            self.vertical_velocity = -self.vertical_velocity

        for i, block in enumerate(blocks):
            if self.rect.colliderect(block.rect):
                self.vertical_velocity = -self.vertical_velocity
                return i
        return -2


class Life:
    max_count = 3
    width = 30
    height = 30

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        asset = pygame.image.load(BaseGame.ASSETS_PATH + "life.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)


class Arcanoid(BaseGame):
    def main(self):
        lifes = []
        level = 1

        ball = Ball(300, 200)
        player = Player(300, 350)
        blocks = Block.spawn()

        for i in range(Life.max_count):
            life = Life(
                BaseGame.WIDTH - Life.width * (Life.max_count - i),
                BaseGame.HEIGHT - Life.height / 2,
            )
            lifes.append(life)

        while True:
            self.clock.tick(60 * level)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif key_down("ESCAPE"):
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BaseGame.BLACK)
            player.draw(self.screen)
            ball.draw(self.screen)
            for block in blocks:
                block.draw(self.screen)
            for life in lifes:
                life.draw(self.screen)

            score_text = self.text_font.render(
                "Score: " + str(self.score), 1, BaseGame.WHITE
            )
            self.screen.blit(score_text, (0, BaseGame.HEIGHT - 30))
            level_text = self.text_font.render(
                "Level: " + str(level), 1, BaseGame.WHITE
            )
            self.screen.blit(level_text, (255, BaseGame.HEIGHT - 30))

            i = ball.move(player, blocks)
            if i == -1:
                if len(lifes) > 1:
                    lifes.pop()
                    ball.__init__(300, 200)
                    player.__init__(300, 350)
                else:
                    self.game_over()
            elif i != -2:
                self.score += 1
                blocks.remove(blocks[i])
                if len(blocks) == 0:
                    blocks = Block.spawn()
                    ball.__init__(300, 200)
                    player.__init__(300, 350)
                    level += 1

            if key_down("LEFT"):
                player.move_left()

            if key_down("RIGHT"):
                player.move_right()

            pygame.display.update()


if __name__ == "__main__":
    game = Arcanoid("Arcanoid")
    game.main()
