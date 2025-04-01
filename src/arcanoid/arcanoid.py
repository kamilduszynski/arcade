# Standard Library Imports
import sys
from random import randint

# Third-party Imports
import pygame

# Local Imports
from base import BaseGame as bg
from tools.utils import key_down


class Player:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = bg.WIDTH / 6
        self.height = 20
        self.velocity = 0
        asset = pygame.image.load(
            bg.ASSETS_PATH + "arcanoid/player.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x += self.velocity

    def move_right(self):
        self.velocity = 4
        self.move()

        if self.rect.x > (bg.WIDTH - self.width):
            self.rect.x = bg.WIDTH - self.width

    def move_left(self):
        self.velocity = -4
        self.move()

        if self.rect.x < 0:
            self.rect.x = 0


class Block:
    width = bg.WIDTH / bg.COLUMN_NUMBER
    height = 20

    def __init__(self, x: int, y: int, block_version: int) -> None:
        self.x = x
        self.y = y
        asset = pygame.image.load(
            bg.ASSETS_PATH + f"arcanoid/block{block_version}.png"
        ).convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.surface):
        screen.blit(self.image, self.rect)

    @staticmethod
    def spawn() -> list:
        blocks = []

        for i in range(bg.ROW_NUMBER):
            for j in range(bg.COLUMN_NUMBER):
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
        asset = pygame.image.load(bg.ASSETS_PATH + "arcanoid/ball.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collisions = 0

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def move(self, player: Player, blocks: list[Block]):
        self.rect.x += self.horizontal_velocity
        self.rect.y += self.vertical_velocity

        if self.rect.x <= 0:
            self.rect.x = 0
            self.horizontal_velocity = -self.horizontal_velocity

        if self.rect.x > bg.WIDTH - self.width:
            self.rect.x = bg.WIDTH - self.width
            self.horizontal_velocity = -self.horizontal_velocity

        if self.rect.y <= 0:
            self.rect.y = 0
            self.vertical_velocity = -self.vertical_velocity

        if self.rect.y >= bg.HEIGHT - self.height:
            return -1

        if self.rect.colliderect(player.rect):
            self.collisions += 1
            randomizer = randint(-10, 10) * 0.1
            self.horizontal_velocity += randomizer
            self.vertical_velocity = -self.vertical_velocity

            if self.collisions >= 10:
                self.rect.y -= 2 * self.height
            return -2

        for i, block in enumerate(blocks):
            if self.rect.colliderect(block.rect):
                self.vertical_velocity = -self.vertical_velocity
                return i
        return -3


class Life:
    max_count = 3
    width = 30
    height = 30

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        asset = pygame.image.load(bg.ASSETS_PATH + "arcanoid/life.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)


class Arcanoid(bg):
    def main(self):
        lifes = []
        level = 1

        ball = Ball(300, 200)
        player = Player(300, 350)
        blocks = Block.spawn()

        for i in range(Life.max_count):
            life = Life(
                bg.WIDTH - Life.width * (Life.max_count - i),
                bg.HEIGHT - Life.height / 2,
            )
            lifes.append(life)

        while True:
            self.clock.tick(60 * level)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or key_down("ESCAPE"):
                    pygame.quit()
                    sys.exit()

            self.screen.fill(bg.BLACK)
            player.draw(self.screen)
            ball.draw(self.screen)
            for block in blocks:
                block.draw(self.screen)
            for life in lifes:
                life.draw(self.screen)

            score_text = self.text_font.render("Score: " + str(self.score), 1, bg.WHITE)
            self.screen.blit(score_text, (0, bg.HEIGHT - 30))
            level_text = self.text_font.render("Level: " + str(level), 1, bg.WHITE)
            self.screen.blit(level_text, (255, bg.HEIGHT - 30))

            if key_down("LEFT"):
                player.move_left()

            if key_down("RIGHT"):
                player.move_right()

            i = ball.move(player, blocks)
            if i == -1:
                if len(lifes) > 1:
                    lifes.pop()
                    ball.__init__(300, 200)
                    player.__init__(300, 350)
                else:
                    self.game_over()
            elif i == -2:
                continue
            elif i >= 0:
                self.score += 1
                blocks.remove(blocks[i])
                if len(blocks) == 0:
                    blocks = Block.spawn()
                    ball.__init__(300, 200)
                    player.__init__(300, 350)
                    level += 1

            ball.collisions = 0
            pygame.display.update()


if __name__ == "__main__":
    game = Arcanoid("Arcanoid", lambda: print("dummy simulation"))
    game.main()
