# Standard Library Imports
import os
import sys
import pickle
from random import randint

# Third-party Imports
import neat
import pygame

# Local Imports
from tools.utils import get_repo_path

GAME_WIDTH = 600
GAME_HEIGHT = 400
ROW_NUMBER = 4
COLUMN_NUMBER = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

gen = 0


class Player:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.width = GAME_WIDTH / 6
        self.height = 20
        self.velocity = 0
        asset = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x += self.velocity

        if self.rect.x < 0:
            self.rect.x = 0

        if self.rect.x > (GAME_WIDTH - self.width):
            self.rect.x = GAME_WIDTH - self.width


class Ball:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.vertical_velocity = 3
        self.horizontal_velocity = randint(-3, 3)
        asset = pygame.image.load("assets/ball.png").convert_alpha()
        self.image = pygame.transform.scale(asset, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, player, blocks):
        self.rect.x += self.horizontal_velocity
        self.rect.y += self.vertical_velocity

        if self.rect.x <= 0:
            self.horizontal_velocity = -self.horizontal_velocity
            self.rect.x += self.horizontal_velocity

        if self.rect.x >= GAME_WIDTH - self.width:
            self.horizontal_velocity = -self.horizontal_velocity
            self.rect.x += self.horizontal_velocity

        if self.rect.y <= 0:
            self.vertical_velocity = -self.vertical_velocity
            self.rect.y += self.vertical_velocity

        if self.rect.y >= GAME_HEIGHT - self.height:
            return -1

        if self.rect.colliderect(player.rect):
            randomizer = randint(-10, 10) * 0.1
            self.horizontal_velocity += randomizer  # + player.velocity/4
            self.vertical_velocity = -self.vertical_velocity
            self.rect.x += self.horizontal_velocity
            self.rect.y += self.vertical_velocity

        for i, block in enumerate(blocks):
            if self.rect.colliderect(block.rect):
                self.vertical_velocity = -self.vertical_velocity
                self.rect.x += self.horizontal_velocity
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


def game_over(screen, text_font):
    game_over_font = pygame.font.Font("assets/pixel_font.ttf", 50)

    while True:
        screen.fill(BLACK)
        gameover_text = game_over_font.render("Game over", 1, WHITE)
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
        clock.tick(60)

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
                game_over(screen, text_font)
        elif i != -2:
            score += 1
            blocks.remove(blocks[i])
            if len(blocks) == 0:
                blocks = spawn_blocks()
                ball.__init__(300, 200)
                player.__init__(300, 350)
                level += 1

        player.velocity = 0

        if get_key("LEFT"):
            player.velocity = -3
            player.move()

        if get_key("RIGHT"):
            player.velocity = 3
            player.move()

        pygame.display.update()


def eval_genomes(genomes, config):
    global gen
    gen += 1

    text_font, clock, screen = game_init()
    nets = []
    balls = []
    players = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        balls.append(Ball(300, 200))
        players.append(Player(300, 350))
        ge.append(genome)

    score = 0
    level = 1
    blocks = spawn_blocks()

    while len(players) > 0:
        clock.tick(170)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif get_key("ESCAPE"):
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        for player in players:
            player.draw(screen)
        for ball in balls:
            ball.draw(screen)
        for block in blocks:
            block.draw(screen)

        score_text = text_font.render("Score: " + str(score), 1, WHITE)
        screen.blit(score_text, (0, GAME_HEIGHT - 30))
        level_text = text_font.render("Level: " + str(level), 1, WHITE)
        screen.blit(level_text, (120, GAME_HEIGHT - 30))
        gen_text = text_font.render("Generation: " + str(gen), 1, WHITE)
        screen.blit(gen_text, (220, GAME_HEIGHT - 30))
        alive_text = text_font.render("Players: " + str(len(players)), 1, WHITE)
        screen.blit(alive_text, (400, GAME_HEIGHT - 30))

        for ball_id, ball in enumerate(balls):
            i = ball.move(players[ball_id], blocks)

            if i == -1:
                players.remove(players[ball_id])
                balls.remove(balls[ball_id])
                ge[ball_id].fitness -= 1
            elif i != -2:
                score += 1
                ge[ball_id].fitness += 1
                blocks.remove(blocks[i])
                if len(blocks) == 0:
                    blocks = spawn_blocks()
                    ball.__init__(300, 200)
                    players[ball_id].__init__(300, 350)
                    level += 1

        player.velocity = 0

        for player_id, player in enumerate(players):
            ge[player_id].fitness += 0.1

            output = nets[player_id].activate(
                (
                    player.rect.x,
                    abs(player.rect.x - balls[player_id].rect.x),
                    balls[player_id].horizontal_velocity,
                )
            )
            print(f"Output: {output}")
            if output[0] > 0.5:
                player.velocity = 3
                player.move()
            else:
                player.velocity = -3
                player.move()

        pygame.display.update()

        if score > 120:
            repo_path = get_repo_path()
            model_path = os.path.join(repo_path, "models/best.pickle")
            pickle.dump(nets[0], open(model_path, "wb"))
            break


def run(config_file):
    # code from https://towardsdatascience.com/ai-teaches-itself-to-play-a-game-f8957a99b628
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print("\nBest genome:\n{!s}".format(winner))


if __name__ == "__main__":
    repo_path = get_repo_path()
    config_path = os.path.join(repo_path, "configs/config.txt")
    run(config_path)
