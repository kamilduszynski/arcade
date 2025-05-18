# Standard Library Imports
import sys
import pickle

# Third-party Imports
import neat
import pygame

# Local Imports
import arcanoid.arcanoid as arc
from tools.utils import key_down


class Trainer:
    def __init__(self):
        self.gen = 0
        self.genomes_list = []
        self.nets = []
        self.balls = []
        self.players = []
        self.game = arc.Arcanoid("Arcanoid", main)

    def eval_genomes(self, genomes, config):
        self.gen += 1

        for _, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.genomes_list.append(genome)
            self.nets.append(net)
            self.balls.append(arc.Ball(300, 200))
            self.players.append(arc.Player(300, 350))

        score = 0
        level = 1
        blocks = arc.Block.spawn()

        while len(self.players) > 0:
            self.game.clock.tick(500)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif key_down("ESCAPE"):
                    pygame.quit()
                    sys.exit()

            self.game.screen.fill(arc.Arcanoid.BLACK)

            for player in self.players:
                player.draw(self.game.screen)
            for ball in self.balls:
                ball.draw(self.game.screen)
            for block in blocks:
                block.draw(self.game.screen)

            score_text = self.game.text_font.render(
                "Score: " + str(score), 1, arc.Arcanoid.WHITE
            )
            self.game.screen.blit(score_text, (0, arc.Arcanoid.HEIGHT - 30))
            level_text = self.game.text_font.render(
                "Level: " + str(level), 1, arc.Arcanoid.WHITE
            )
            self.game.screen.blit(level_text, (120, arc.Arcanoid.HEIGHT - 30))
            gen_text = self.game.text_font.render(
                "Generation: " + str(self.gen), 1, arc.Arcanoid.WHITE
            )
            self.game.screen.blit(gen_text, (220, arc.Arcanoid.HEIGHT - 30))
            alive_text = self.game.text_font.render(
                "Players: " + str(len(self.players)), 1, arc.Arcanoid.WHITE
            )
            self.game.screen.blit(alive_text, (400, arc.Arcanoid.HEIGHT - 30))

            for player_id, player in enumerate(self.players):
                self.genomes_list[player_id].fitness += 0.1

                output = self.nets[player_id].activate(
                    (
                        player.rect.x,
                        abs(player.rect.x - self.balls[player_id].rect.x),
                        self.balls[player_id].horizontal_velocity,
                    )
                )
                move_player(player, output)

                if score > 120 or self.genomes_list[player_id].fitness > 1000:
                    pickle.dump(
                        self.nets[player_id],
                        open(arc.Arcanoid.MODEL_PATH, "wb"),
                    )

            for ball_id, ball in enumerate(self.balls):
                i = ball.move(self.players[ball_id], blocks)

                if i == -1:
                    self.players.remove(self.players[ball_id])
                    self.balls.remove(self.balls[ball_id])
                    self.genomes_list[ball_id].fitness -= 10
                elif i == -2:
                    continue
                elif i >= 0:
                    score += 1
                    self.genomes_list[ball_id].fitness += 10
                    blocks.remove(blocks[i])
                    if len(blocks) == 0:
                        blocks = arc.Block.spawn()
                        ball.__init__(300, 200)
                        self.players[ball_id].__init__(300, 350)
                        level += 1
                ball.collisions = 0

            pygame.display.update()

    def run_best_genome(self):
        with open(arc.Arcanoid.MODEL_PATH, "rb") as file:
            best_genome = pickle.load(file)

        net = best_genome
        ball = arc.Ball(300, 200)
        player = arc.Player(300, 350)

        score = 0
        level = 1
        blocks = arc.Block.spawn()

        while True > 0:
            self.game.clock.tick(60 * level)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif key_down("ESCAPE"):
                    pygame.quit()
                    sys.exit()

            self.game.screen.fill(arc.Arcanoid.BLACK)

            player.draw(self.game.screen)
            ball.draw(self.game.screen)
            for block in blocks:
                block.draw(self.game.screen)

            score_text = self.game.text_font.render(
                "Score: " + str(score), 1, arc.Arcanoid.WHITE
            )
            self.game.screen.blit(score_text, (0, arc.Arcanoid.HEIGHT - 30))
            level_text = self.game.text_font.render(
                "Level: " + str(level), 1, arc.Arcanoid.WHITE
            )
            self.game.screen.blit(level_text, (255, arc.Arcanoid.HEIGHT - 30))

            i = ball.move(player, blocks)
            output = net.activate(
                (
                    player.rect.x,
                    abs(player.rect.x - ball.rect.x),
                    ball.horizontal_velocity,
                )
            )
            move_player(player, output)

            if i == -1:
                pygame.quit()
                sys.exit()
            elif i == -2:
                continue
            elif i >= 0:
                score += 1
                blocks.remove(blocks[i])
                if len(blocks) == 0:
                    blocks = arc.Block.spawn()
                    ball.__init__(300, 200)
                    player.__init__(300, 350)
                    level += 1

            ball.collisions = 0
            pygame.display.update()

    def run_neat(self, config_file, generations=50):
        # code from https://towardsdatascience.com/ai-teaches-itself-to-play-a-self.game-f8957a99b628
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
            generation_interval=10,
            filename_prefix=arc.Arcanoid.CHECKPOINT_PATH,
        )
        p.add_reporter(checkpointer)

        # Run for up to 50 generations.
        winner = p.run(fitness_function=self.eval_genomes, n=generations)

        # show final stats
        print(f"\nBest genome:\n{str(winner)}")


def move_player(player, output):
    print("Output:", output)
    if output[0] > 0.9:
        player.move_right()
    elif output[0] < -0.9:
        player.move_left()


def main():
    trainer = Trainer()
    trainer.run_neat(arc.Arcanoid.CONFIGS_PATH + "config.txt", 5)
    trainer.run_best_genome()


if __name__ == "__main__":
    main()
