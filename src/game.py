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
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.width = GAME_WIDTH / 6
        self.height = 20
        self.velocity = 3
        asset = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move_left(self):
        self.rect.x -= self.velocity

        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self):
        self.rect.x += self.velocity

        if self.rect.x > (GAME_WIDTH - self.width):
            self.rect.x = GAME_WIDTH - self.width


class Ball:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.vertical_velocity = 3
        self.horizonal_velocity = randint(-3, 3)
        asset = pygame.image.load("assets/ball.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, player_rect, blocks):
        self.rect.x += self.horizonal_velocity
        self.rect.y += self.vertical_velocity

        if self.rect.x <= 0:
            self.horizonal_velocity = -self.horizonal_velocity
            self.rect.x += self.horizonal_velocity

        if self.rect.x >= GAME_WIDTH - self.width:
            self.horizonal_velocity = -self.horizonal_velocity
            self.rect.x += self.horizonal_velocity

        if self.rect.y <= 0:
            self.vertical_velocity = -self.vertical_velocity
            self.rect.y += self.vertical_velocity

        if self.rect.y >= GAME_HEIGHT - self.height:
            return -1

        if self.rect.colliderect(player_rect):
            randomizer = randint(-10, 10) * 0.1
            self.horizonal_velocity += randomizer
            self.vertical_velocity = -self.vertical_velocity
            self.rect.x += self.horizonal_velocity
            self.rect.y += self.vertical_velocity

        for i, block in enumerate(blocks):
            if self.rect.colliderect(block.rect):
                self.vertical_velocity = -self.vertical_velocity
                self.rect.x += self.horizonal_velocity
                self.rect.y += self.vertical_velocity
                return i
        return -2


class Block:
    width = GAME_WIDTH / COLUMN_NUMBER
    height = 20

    def __init__(self, x, y, block_var) -> None:
        self.x = x
        self.y = y
        asset = pygame.image.load(f"assets/block{block_var}.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Life:
    max_count = 3
    width = 30
    height = 30

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        asset = pygame.image.load(f"assets/life.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def get_key(keyName):
    key_is_pressed = False
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, f"K_{keyName}")
    if keyInput[myKey]:
        key_is_pressed = True
    return key_is_pressed


def game_over(screen, text_font):
    gameover_font = pygame.font.Font("assets/pixel_font.ttf", 50)

    while True:
        screen.fill(BLACK)
        gameover_text = gameover_font.render("Game over", 1, WHITE)
        screen.blit(gameover_text, (160, 100))
        restart_text = text_font.render("Press space to play again", 1, WHITE)
        screen.blit(restart_text, (160, 200))
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
    pygame.init()
    pygame.display.set_caption("Arcanoid")

    text_font = pygame.font.Font("assets/pixel_font.ttf", 20)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    player = Player(300, 350)
    ball = Ball(300, 200)
    blocks = []
    lifes = []

    for i in range(ROW_NUMBER):
        for j in range(COLUMN_NUMBER):
            block = Block(
                j * Block.width + Block.width / 2,
                i * Block.height + Block.height / 2,
                (j + i) % 4,
            )
            blocks.append(block)

    for i in range(Life.max_count):
        life = Life(
            GAME_WIDTH - Life.width * (Life.max_count - i),
            GAME_HEIGHT - Life.height / 2,
        )
        lifes.append(life)

    while True:
        clock.tick(60)
        screen.fill(BLACK)
        player.draw(screen)
        ball.draw(screen)
        for block in blocks:
            block.draw(screen)
        for life in lifes:
            life.draw(screen)

        score = COLUMN_NUMBER * ROW_NUMBER - len(blocks)

        score_text = text_font.render("Score: " + str(score), 1, WHITE)
        screen.blit(score_text, (0, GAME_HEIGHT - 30))

        i = ball.move(player.rect, blocks)
        if i == -1:
            if len(lifes) > 0:
                lifes.pop()
                ball.__init__(300, 200)
                player.__init__(300, 350)
            else:
                game_over(screen, text_font)
        elif i != -2:
            blocks.remove(blocks[i])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif get_key("ESCAPE"):
                pygame.quit()
                sys.exit()

        if get_key("LEFT"):
            player.move_left()

        if get_key("RIGHT"):
            player.move_right()

        pygame.display.update()


if __name__ == "__main__":
    arcanoid()
