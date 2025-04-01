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
        self.width = 20
        self.height = 20
        self.direction = "DOWN"

        asset = pygame.image.load(bg.ASSETS_PATH + "snake/player.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def move(self) -> None:
        match self.direction:
            case "LEFT":
                self.rect.x -= self.width
                if self.rect.x < self.width:
                    self.rect.x = bg.WIDTH - 2 * self.width
            case "RIGHT":
                self.rect.x += self.width
                if self.rect.x > bg.WIDTH - 1.5 * self.width:
                    self.rect.x = 2 * self.width
            case "UP":
                self.rect.y -= self.height
                if self.rect.y < self.height:
                    self.rect.y = bg.HEIGHT - 2 * self.height
            case "DOWN":
                self.rect.y += self.height
                if self.rect.y > bg.HEIGHT - 1.5 * self.height:
                    self.rect.y = 2 * self.height


class Border:
    def __init__(self) -> None:
        self.width = 40
        self.height = 40

        asset = pygame.image.load(bg.ASSETS_PATH + "snake/border.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))

    def draw(self, screen: pygame.Surface) -> None:
        for x in range(int(bg.WIDTH / self.width)):
            self.rect = self.image.get_rect(center=(x * self.width, 0))
            screen.blit(self.image, self.rect)

        for x in range(int(bg.WIDTH / self.width)):
            self.rect = self.image.get_rect(center=(x * self.width, bg.HEIGHT))
            screen.blit(self.image, self.rect)

        for y in range(int(bg.HEIGHT / self.height)):
            self.rect = self.image.get_rect(center=(0, y * self.height))
            screen.blit(self.image, self.rect)

        for y in range(int(bg.HEIGHT / self.height)):
            self.rect = self.image.get_rect(center=(bg.WIDTH, y * self.height))
            screen.blit(self.image, self.rect)

        self.rect = self.image.get_rect(center=(bg.WIDTH, bg.HEIGHT))
        screen.blit(self.image, self.rect)


class Food:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20

        asset = pygame.image.load(bg.ASSETS_PATH + "snake/mouse.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)


class Snake(bg):
    def main(self):
        level = 1
        border = Border()
        player = Player(130, 130)

        x = randint(1, int(bg.WIDTH / 20) - 1) * 20 + 10
        y = randint(1, int(bg.HEIGHT / 20) - 1) * 20 + 10
        food = Food(x, y)

        while True:
            self.clock.tick(10 * level)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or key_down("ESCAPE"):
                    pygame.quit()
                    sys.exit()

            self.screen.fill(bg.BLACK)

            border.draw(self.screen)
            player.draw(self.screen)
            food.draw(self.screen)

            score_text = self.text_font.render("Score: " + str(self.score), 1, bg.WHITE)
            self.screen.blit(score_text, (2, bg.HEIGHT - 22))
            level_text = self.text_font.render("Level: " + str(level), 1, bg.WHITE)
            self.screen.blit(level_text, (255, bg.HEIGHT - 22))

            player.move()

            if key_down("LEFT"):
                player.direction = "LEFT"

            if key_down("RIGHT"):
                player.direction = "RIGHT"

            if key_down("UP"):
                player.direction = "UP"

            if key_down("DOWN"):
                player.direction = "DOWN"

            pygame.display.update()
