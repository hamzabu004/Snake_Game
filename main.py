import time
import random
import pygame
from pygame.locals import *
from tkinter import *
from tkinter import messagebox


SIZE = 40


class Apple:
    def __init__(self, p_screen):
        self.p_screen = p_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.p_screen.blit(self.apple, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(0, 19) * SIZE
        self.y = random.randint(0, 14) * SIZE


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 600))
        self.surface.fill((255, 255, 255))
        pygame.display.update()
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def is_collided(self, x1, y1, x2, y2):
        # if x2 <= x1 < x2 + SIZE:
        #     if y2 <= y1 < y2 + SIZE:
        if y2 == y1 and x2 == x1:
            return True
        return False

    def dup_ckr_apple(self):
        for i in self.snake.x:
            if i == self.apple.x:
                for j in self.snake.y:
                    if j == self.apple.y:
                        return True
        return False

    def disp_score(self):
        font = pygame.font.SysFont("calibre", 40)
        score = font.render(f"Score: {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(score, (650, 20))

    def collid_wall(self):
        if 800 < self.snake.x[0] or self.snake.x[0] < 0 or 600 < self.snake.y[0] or self.snake.y[0] < 0:
            return True
        return False

    def play_sound(self, s_name):
        sound = pygame.mixer.Sound(f"resources/{s_name}.mp3")
        pygame.mixer.Sound.play(sound)


    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.disp_score()
        pygame.display.update()

        # snake with apple
        if self.is_collided(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y) :
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()
            while self.dup_ckr_apple():
                self.apple.move()
            self.apple.draw()

        # snake with itself
        for i in range(3, self.snake.length):
            if self.is_collided(self.snake.x[0], self.snake.y[0], self.snake.x[i],  self.snake.y[i]) or self.collid_wall():
                print("Game Over", f"Score : {self.snake.length}", sep='\n')
                raise "Game Over"
        if self.collid_wall():
            print("Game Over", f"Score : {self.snake.length}", sep='\n')
            raise "Game Over"

    def run(self):
        run_state = True
        while run_state:
            for event in pygame.event.get():
                if event.type == QUIT:
                    run_state = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run_state = False
                    elif event.key == K_UP:
                        if self.snake.direction != "down":
                            self.snake.move_up()
                            break
                    elif event.key == K_DOWN:
                        if self.snake.direction != "up":
                            self.snake.move_down()
                            break
                    elif event.key == K_LEFT:
                        if self.snake.direction != "right":
                            self.snake.move_left()
                            break
                    elif event.key == K_RIGHT:
                        if self.snake.direction != "left":
                            self.snake.move_right()
                            break
            try:
                self.play()
            except Exception as e:
                pygame.mixer.music.pause()
                Tk().wm_withdraw() #to hide the main window
                answer = messagebox.askyesno("Game Over!", "Press ok to play again")
                if answer:
                    Tk().destroy()
                    self.snake = Snake(self.surface, 1)
                    self.apple = Apple(self.surface)
                    pygame.display.update()
                    pygame.mixer.music.unpause()

                else:
                    exit(0)
            
            time.sleep(.1)


class Snake:
    def __init__(self, p_screen, length):
        self.p_screen = p_screen
        self.black_block = pygame.image.load("resources/block_black.png").convert()
        self.orange_block = pygame.image.load("resources/block_orange.png").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.main_block = None
        self.length = length
        self.direction = "down"

    def draw(self):
        self.p_screen.fill((255, 255, 255))

        for i in range(self.length):
            if (i+1) % 2 != 0:
                self.main_block = self .black_block
            else:
                self.main_block = self .orange_block
            self.p_screen.blit(self.main_block, (self.x[i], self.y[i]))
        pygame.display.update()

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == "down":
            self.y[0] += SIZE
        elif self.direction == "up":
            self.y[0] -= SIZE
        elif self.direction == "left":
            self.x[0] -= SIZE
        elif self.direction == "right":
            self.x[0] += SIZE

        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


# check if program is running itself (! if from other script)
if __name__ == "__main__":
    game = Game()
    game.run()
