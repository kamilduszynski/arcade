# Standard Library Imports
import sys
from random import randint

# Third-party Imports
import pygame

GAME_WIDTH = 600
GAME_HEIGHT = 400
ROW_NUMBER = 4
COLUMN_NUMBER = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Player:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = GAME_WIDTH / 6
        self.height = 20
        self.velocity = 3
        asset = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def move_right(self):
        self.rect.x += self.velocity

        if self.rect.x > (GAME_WIDTH - self.width):
            self.rect.x = GAME_WIDTH - self.width

    def move_left(self):
        self.rect.x -= self.velocity

        if self.rect.x < 0:
            self.rect.x = 0


class Block:
    width = GAME_WIDTH / COLUMN_NUMBER
    height = 20

    def __init__(self, x: int, y: int, block_version: int) -> None:
        self.x = x
        self.y = y
        asset = pygame.image.load(f"assets/block{block_version}.png").convert_alpha()
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
        asset = pygame.image.load("assets/ball.png").convert_alpha()
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

        if self.rect.x > GAME_WIDTH - self.width:
            self.rect.x = GAME_WIDTH - self.width
            self.horizontal_velocity = -self.horizontal_velocity

        if self.rect.y <= 0:
            self.rect.y = 0
            self.vertical_velocity = -self.vertical_velocity

        if self.rect.y >= GAME_HEIGHT - self.height:
            return -1

        if self.rect.colliderect(player.rect):
            # randomizer = randint(-10, 10) * 0.1
            self.horizontal_velocity += player.velocity  # + randomizer
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
        asset = pygame.image.load(f"assets/life.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)


def get_key(keyName: str):
    key_is_pressed = False
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, f"K_{keyName}")
    if keyInput[myKey]:
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

    text_font = pygame.font.Font("assets/pixel_font.ttf", 20)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    return text_font, clock, screen


def game_over(screen: pygame.Surface, text_font: pygame.font.Font, score: int):
    game_over_font = pygame.font.Font("assets/pixel_font.ttf", 50)
    game_over_score_font = pygame.font.Font("assets/pixel_font.ttf", 35)

    while True:
        screen.fill(BLACK)
        gameover_text = game_over_font.render("Game over", 1, WHITE)
        screen.blit(gameover_text, (160, 100))
        gameover_text = game_over_score_font.render(f"Score: {score}", 1, WHITE)
        screen.blit(gameover_text, (210, 180))
        restart_text = text_font.render("Press space to play again", 1, WHITE)
        screen.blit(restart_text, (160, 240))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif get_key("ESCAPE"):
                pygame.quit()
                sys.exit()
            elif get_key("SPACE"):
                arcanoid()
        pygame.display.update()


def arcanoid():
    text_font, clock, screen = game_init()
    player = Player(300, 350)
    ball = Ball(300, 200)
    lifes = []
    score = 0
    level = 1
    blocks = spawn_blocks()

    for i in range(Life.max_count):
        life = Life(
            GAME_WIDTH - Life.width * (Life.max_count - i),
            GAME_HEIGHT - Life.height / 2,
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
        screen.blit(score_text, (0, GAME_HEIGHT - 30))
        level_text = text_font.render("Level: " + str(level), 1, WHITE)
        screen.blit(level_text, (255, GAME_HEIGHT - 30))

        i = ball.move(player, blocks)
        if i == -1:
            if len(lifes) > 1:
                lifes.pop()
                ball.__init__(300, 200)
                player.__init__(300, 350)
            else:
                game_over(screen, text_font, score)
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
    arcanoid()
