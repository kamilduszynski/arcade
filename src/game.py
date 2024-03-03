# Standard Library Imports
import sys

# Third-party Imports
import pygame

LEFT_BORDER = 0
RIGHT_BORDER = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Player:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.velocity = 3
        asset = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (140, 20))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        print(self.x)
        screen.blit(self.image, self.rect)

    def move_left(self):
        self.rect.x -= self.velocity

        if self.rect.x < LEFT_BORDER:
            self.rect.x = LEFT_BORDER

    def move_right(self):
        self.rect.x += self.velocity

        if self.rect.x > (RIGHT_BORDER - 140):
            self.rect.x = RIGHT_BORDER - 140


def getKey(keyName):
    key_is_pressed = False
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, f"K_{keyName}")
    if keyInput[myKey]:
        key_is_pressed = True
    return key_is_pressed


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Arcanoid")

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600, 400))
    player = Player(230, 360)

    while True:
        clock.tick(60)
        screen.fill(WHITE)
        player.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif getKey("ESCAPE"):
                pygame.quit()
                sys.exit()

        if getKey("LEFT"):
            player.move_left()

        if getKey("RIGHT"):
            player.move_right()

        pygame.display.update()
