# Standard Library Imports
import os
import sys
from random import randint

# Third-party Imports
import pygame

# Local Imports
from main import main_menu
from tools.utils import get_repo_path

# Global Variables
gen = 0
repo_path = get_repo_path()

ASSETS_PATH = os.path.join(repo_path, "assets/")
CONFIGS_PATH = os.path.join(repo_path, "configs/")

MODEL_PATH = os.path.join(repo_path, "models/best_genome.pickle")
CHEKCPOINT_PATH = os.path.join(repo_path, "models/neat-checkpoint-")

WIDTH = 600
HEIGHT = 400
ROW_NUMBER = 4
COLUMN_NUMBER = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Player:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = WIDTH / 6
        self.height = 20
        self.velocity = 0
        asset = pygame.image.load(ASSETS_PATH + "player.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x += self.velocity

    def move_right(self):
        self.velocity = 4
        self.move()

        if self.rect.x > (WIDTH - self.width):
            self.rect.x = WIDTH - self.width

    def move_left(self):
        self.velocity = -4
        self.move()

        if self.rect.x < 0:
            self.rect.x = 0


class Block:
    width = WIDTH / COLUMN_NUMBER
    height = 20

    def __init__(self, x: int, y: int, block_version: int) -> None:
        self.x = x
        self.y = y
        asset = pygame.image.load(
            ASSETS_PATH + f"block{block_version}.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.surface):
        screen.blit(self.image, self.rect)


class Ball:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.vertical_velocity = 3
        self.horizontal_velocity = randint(-3, 3)
        asset = pygame.image.load(ASSETS_PATH + "ball.png").convert_alpha()
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

        if self.rect.x > WIDTH - self.width:
            self.rect.x = WIDTH - self.width
            self.horizontal_velocity = -self.horizontal_velocity

        if self.rect.y <= 0:
            self.rect.y = 0
            self.vertical_velocity = -self.vertical_velocity

        if self.rect.y >= HEIGHT - self.height:
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
        asset = pygame.image.load(ASSETS_PATH + "life.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)


def get_key(key_name: str):
    key_is_pressed = False
    key_input = pygame.key.get_pressed()
    key = getattr(pygame, f"K_{key_name}")
    if key_input[key]:
        key_is_pressed = True
    return key_is_pressed


def spawn_blocks():
    blocks = []

    for i in range(ROW_NUMBER):
        for j in range(COLUMN_NUMBER):
            block = Block(
                j * Block.width + Block.width / 2,
                i * Block.height + Block.height / 2,
                (j + i) % 4,
            )
            blocks.append(block)
    return blocks


def game_init():
    pygame.init()
    pygame.display.set_caption("Arcanoid")
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    text_font = pygame.font.Font(ASSETS_PATH + "pixel_font.ttf", 20)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    return text_font, clock, screen


def game_over(
    text_font: pygame.font.Font,
    clock: pygame.time.Clock,
    screen: pygame.Surface,
    score: int,
):
    game_over_font = pygame.font.Font(ASSETS_PATH + "pixel_font.ttf", 50)
    game_over_score_font = pygame.font.Font(ASSETS_PATH + "pixel_font.ttf", 35)

    while True:
        screen.fill(BLACK)
        game_over_text = game_over_font.render("Game over", 1, WHITE)
        screen.blit(game_over_text, (160, 80))
        game_over_text = game_over_score_font.render(f"Score: {score}", 1, WHITE)
        screen.blit(game_over_text, (210, 150))
        restart_text = text_font.render("Press space to play again", 1, WHITE)
        screen.blit(restart_text, (160, 240))
        restart_text = text_font.render("Press enter to go back to main menu", 1, WHITE)
        screen.blit(restart_text, (110, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif get_key("ESCAPE"):
                pygame.quit()
                sys.exit()
            elif get_key("SPACE"):
                main(text_font, clock, screen)
            elif get_key("RETURN"):
                main_menu()
        pygame.display.update()


def main(text_font: pygame.font.Font, clock: pygame.time.Clock, screen: pygame.Surface):
    player = Player(300, 350)
    ball = Ball(300, 200)
    lifes = []
    score = 0
    level = 1
    blocks = spawn_blocks()

    for i in range(Life.max_count):
        life = Life(
            WIDTH - Life.width * (Life.max_count - i),
            HEIGHT - Life.height / 2,
        )
        lifes.append(life)

    while True:
        clock.tick(60 * level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif get_key("ESCAPE"):
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        player.draw(screen)
        ball.draw(screen)
        for block in blocks:
            block.draw(screen)
        for life in lifes:
            life.draw(screen)

        score_text = text_font.render("Score: " + str(score), 1, WHITE)
        screen.blit(score_text, (0, HEIGHT - 30))
        level_text = text_font.render("Level: " + str(level), 1, WHITE)
        screen.blit(level_text, (255, HEIGHT - 30))

        i = ball.move(player, blocks)
        if i == -1:
            if len(lifes) > 1:
                lifes.pop()
                ball.__init__(300, 200)
                player.__init__(300, 350)
            else:
                game_over(text_font, clock, screen, score)
        elif i != -2:
            score += 1
            blocks.remove(blocks[i])
            if len(blocks) == 0:
                blocks = spawn_blocks()
                ball.__init__(300, 200)
                player.__init__(300, 350)
                level += 1

        if get_key("LEFT"):
            player.move_left()

        if get_key("RIGHT"):
            player.move_right()

        pygame.display.update()


if __name__ == "__main__":
    main()
