import pygame
import sys
import random
import time

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 720, 480
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 0, 0)
SNAKE_SIZE = 10

# Initialize pygame
pygame.init()

# Screen configuration
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock for controlling the frame rate
clock = pygame.time.Clock()


class SnakeGame:
    def __init__(self, difficulty):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_pos = [random.randrange(
            1, WINDOW_WIDTH // 10) * 10, random.randrange(1, WINDOW_HEIGHT // 10) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.score = 0
        self.difficulty = difficulty

    def move(self, change_to):
        if change_to in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            self.direction = change_to

        if self.direction == 'UP':
            self.snake_pos[1] -= SNAKE_SIZE
        elif self.direction == 'DOWN':
            self.snake_pos[1] += SNAKE_SIZE
        elif self.direction == 'LEFT':
            self.snake_pos[0] -= SNAKE_SIZE
        elif self.direction == 'RIGHT':
            self.snake_pos[0] += SNAKE_SIZE

    def grow(self):
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos == self.food_pos:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        if not self.food_spawn:
            self.food_pos = [random.randrange(
                1, WINDOW_WIDTH // 10) * 10, random.randrange(1, WINDOW_HEIGHT // 10) * 10]
        self.food_spawn = True

    def check_game_over(self):
        if self.snake_pos[0] < 0 or self.snake_pos[0] > WINDOW_WIDTH - SNAKE_SIZE or \
           self.snake_pos[1] < 0 or self.snake_pos[1] > WINDOW_HEIGHT - SNAKE_SIZE or \
           self.snake_pos in self.snake_body[1:]:
            self._game_over()

    def _game_over(self):
        font = pygame.font.SysFont('arial', 60)
        GO_surf = font.render('Your Score is : ' +
                              str(self.score), True, TEXT_COLOR)
        GO_rect = GO_surf.get_rect()
        GO_rect.midtop = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        screen.blit(GO_surf, GO_rect)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    def draw_elements(self):
        screen.fill(BACKGROUND_COLOR)
        for pos in self.snake_body:
            pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(
                pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))

        pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(
            self.food_pos[0], self.food_pos[1], SNAKE_SIZE, SNAKE_SIZE))
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, ord('w')] and not self.direction == 'DOWN':
                        self.move('UP')
                    elif event.key in [pygame.K_DOWN, ord('s')] and not self.direction == 'UP':
                        self.move('DOWN')
                    elif event.key in [pygame.K_LEFT, ord('a')] and not self.direction == 'RIGHT':
                        self.move('LEFT')
                    elif event.key in [pygame.K_RIGHT, ord('d')] and not self.direction == 'LEFT':
                        self.move('RIGHT')

            self.move(self.direction)
            self.grow()
            self.check_game_over()
            self.draw_elements()
            clock.tick(self.difficulty)


# Create a game instance and run the game
game = SnakeGame(difficulty=25)
game.run()
