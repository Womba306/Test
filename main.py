import pygame
import sys
import random
import time
while True:
    print("Выберите режим 1 - играете вы | 2 - играет автопилот")
    YourSetings = int(input())
    if YourSetings==1 or YourSetings==2:
        break
class Game():
    def __init__(self):
        self.screen_width = 720
        self.screen_height = 460
        self.red = pygame.Color(255,0,0)
        self.green = pygame.Color(0, 0, 255)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(0, 0, 0)
        self.brown = pygame.Color(165, 42, 42)
        self.fps_controller = pygame.time.Clock()
        self.score=0

    def init_and_check_for_errors(self):
        check_errors=pygame.init()
        if check_errors[1]>0:
            sys.exit()
        else:
            print("Let`s GOOOOO!")
    def set_surface_and_title(self):
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
    def event_loop(self, change_to):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to
    def refresh_screen(self):
        pygame.display.flip()
        game.fps_controller.tick(60)
    def show_score(self, choice=1):
        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render('Score: {0}'.format(self.score), True, self.white)

        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (80, 10)
        else:
            s_rect.midtop = (360, 120)
    def game_over(self):
        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

class Snake():
    def __init__(self, snake_color):
        self.snake_head_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        self.direction = "RIGHT"
        self.change_to = self.direction
    def validate_direction_and_change(self):
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",self.change_to == "LEFT" and not self.direction == "RIGHT",self.change_to == "UP" and not self.direction == "DOWN",self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def auto_validate_direction_and_change(self, screen_width, screen_height):
        scope=0
        if self.snake_head_pos[0] == screen_width - 10:
            self.direction = "DOWN"
        if self.snake_head_pos[1] == screen_height - 10:
            self.direction = "LEFT"
        if self.snake_head_pos[1] == screen_height -10  and self.snake_head_pos[0] == 0:
            self.direction = "UP"
        if self.snake_head_pos[1] == 0 and self.snake_head_pos[0] == 0:
            self.direction = "RIGHT"
        if self.snake_head_pos[1] == 0 and self.snake_head_pos[0] == 10:
            while self.snake_head_pos[1] != screen_height-10  and self.snake_head_pos[0] != screen_width-10:
                if self.snake_head_pos[1] == 0 and scope==0:
                    self.direction = "DOWN"
                    scope = 1
                if self.snake_head_pos[1] == screen_height - 20 and scope==1:
                    self.direction = "LEFT"
                    scope = 2
                if self.snake_head_pos[1] == screen_height - 20 and scope==2:
                    self.direction = "UP"
                    scope = 0
        self.change_to = self.direction
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to


    def change_head_position(self):
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        if (self.snake_head_pos[0] == food_pos[0] and self.snake_head_pos[1] == food_pos[1]):
            food_pos = [random.randrange(1, screen_width / 10) * 10,random.randrange(1, screen_height / 10) * 10]
            score += 1
        else:
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(play_surface, self.snake_color, pygame.Rect(pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        if any((self.snake_head_pos[0] > screen_width-10 or self.snake_head_pos[0] < 0, self.snake_head_pos[1] >
screen_height-10 or self.snake_head_pos[1] < 0)):
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and block[1] == self.snake_head_pos[1]):
                game_over()
class Food():
    def __init__(self, food_color, screen_width, screen_height):
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width / 10) * 10,random.randrange(1, screen_height / 10) * 10]
    def draw_food(self, play_surface):
        pygame.draw.rect(play_surface, self.food_color, pygame.Rect(self.food_pos[0], self.food_pos[1],self.food_size_x, self.food_size_y))
game = Game()
snake = Snake(game.green)
food = Food(game.brown, game.screen_width, game.screen_height)
game.init_and_check_for_errors()
game.set_surface_and_title()

while True:
    snake.change_to = game.event_loop(snake.change_to)
    if YourSetings==1:
        snake.validate_direction_and_change()
    else:
        snake.auto_validate_direction_and_change(game.screen_width, game.screen_height)

    snake.change_head_position()
    game.score, food.food_pos = snake.snake_body_mechanism(game.score, food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.play_surface, game.white)
    food.draw_food(game.play_surface)
    print(snake.snake_head_pos[0], snake.snake_head_pos[1])
    snake.check_for_boundaries(game.game_over, game.screen_width, game.screen_height)
    game.show_score()
    game.refresh_screen()

