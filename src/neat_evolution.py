# Standard Library Imports
import os
import sys
import pickle

# Third-party Imports
import neat
import pygame

# Local Imports
import arcanoid
from tools.utils import get_repo_path

# Global Variables
gen = 0
repo_path = get_repo_path()
config_path = os.path.join(repo_path, "configs/config.txt")
model_path = os.path.join(repo_path, "models/best_genome.pickle")
checkpoint_path = os.path.join(repo_path, "models/neat-checkpoint-")


def eval_genomes(genomes, config):
    global gen
    # global repo_path
    # global model_path
    gen += 1

    text_font, clock, screen = arcanoid.game_init()
    ge = []
    nets = []
    balls = []
    players = []

    for _, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        ge.append(genome)
        nets.append(net)
        balls.append(arcanoid.Ball(300, 200))
        players.append(arcanoid.Player(300, 350))

    score = 0
    level = 1
    blocks = arcanoid.spawn_blocks()

    while len(players) > 0:
        clock.tick(500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif arcanoid.get_key("ESCAPE"):
                pygame.quit()
                sys.exit()

        screen.fill(arcanoid.BLACK)

        for player in players:
            player.draw(screen)
        for ball in balls:
            ball.draw(screen)
        for block in blocks:
            block.draw(screen)

        score_text = text_font.render("Score: " + str(score), 1, arcanoid.WHITE)
        screen.blit(score_text, (0, arcanoid.GAME_HEIGHT - 30))
        level_text = text_font.render("Level: " + str(level), 1, arcanoid.WHITE)
        screen.blit(level_text, (120, arcanoid.GAME_HEIGHT - 30))
        gen_text = text_font.render("Generation: " + str(gen), 1, arcanoid.WHITE)
        screen.blit(gen_text, (220, arcanoid.GAME_HEIGHT - 30))
        alive_text = text_font.render(
            "Players: " + str(len(players)), 1, arcanoid.WHITE
        )
        screen.blit(alive_text, (400, arcanoid.GAME_HEIGHT - 30))

        for ball_id, ball in enumerate(balls):
            i = ball.move(players[ball_id], blocks)

            if i == -1:
                players.remove(players[ball_id])
                balls.remove(balls[ball_id])
                ge[ball_id].fitness -= 10
            elif i != -2:
                score += 1
                ge[ball_id].fitness += 10
                blocks.remove(blocks[i])
                if len(blocks) == 0:
                    blocks = arcanoid.spawn_blocks()
                    ball.__init__(300, 200)
                    players[ball_id].__init__(300, 350)
                    level += 1

        for player_id, player in enumerate(players):
            ge[player_id].fitness += 0.1

            output = nets[player_id].activate(
                (
                    player.rect.x,
                    abs(player.rect.x - balls[player_id].rect.x),
                    balls[player_id].horizontal_velocity,
                )
            )
            if output[0] > 0.5:
                player.move_right()
            elif output[0] < -0.5:
                player.move_left()

            if score > 120 or ge[player_id].fitness > 1000:
                pickle.dump(nets[player_id], open(model_path, "wb"))

        pygame.display.update()


def run_best_genome():
    text_font, clock, screen = arcanoid.game_init()

    with open(model_path, "rb") as file:
        best_genome = pickle.load(file)

    net = best_genome
    ball = arcanoid.Ball(300, 200)
    player = arcanoid.Player(300, 350)

    score = 0
    level = 1
    blocks = arcanoid.spawn_blocks()

    while True > 0:
        clock.tick(240)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif arcanoid.get_key("ESCAPE"):
                pygame.quit()
                sys.exit()

        screen.fill(arcanoid.BLACK)

        player.draw(screen)
        ball.draw(screen)
        for block in blocks:
            block.draw(screen)

        score_text = text_font.render("Score: " + str(score), 1, arcanoid.WHITE)
        screen.blit(score_text, (0, arcanoid.GAME_HEIGHT - 30))
        level_text = text_font.render("Level: " + str(level), 1, arcanoid.WHITE)
        screen.blit(level_text, (255, arcanoid.GAME_HEIGHT - 30))

        i = ball.move(player, blocks)

        if i == -1:
            arcanoid.game_over(screen, text_font, score)
        elif i != -2:
            score += 1
            blocks.remove(blocks[i])
            if len(blocks) == 0:
                blocks = arcanoid.spawn_blocks()
                ball.__init__(300, 200)
                player.__init__(300, 350)
                level += 1

        output = net.activate(
            (
                player.rect.x,
                abs(player.rect.x - ball.rect.x),
                ball.horizontal_velocity,
            )
        )

        if output[0] > 0.5:
            player.move_right()
        elif output[0] < -0.5:
            player.move_left()

        pygame.display.update()


def run_neat(config_file, generations=50):
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
    checkpointer = neat.Checkpointer(
        generation_interval=10, filename_prefix=checkpoint_path
    )
    p.add_reporter(checkpointer)

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, generations)

    # show final stats
    print(f"\nBest genome:\n{str(winner)}")


if __name__ == "__main__":
    run_neat(config_path, 50)
    run_best_genome()
