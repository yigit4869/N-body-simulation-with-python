import pygame
import itertools
from sys import exit
import random
import math


pygame.init()
WINDOW_SIZE = (1000,1000)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
CLOCK = pygame.time.Clock()

BACKGROUND = pygame.Surface(WINDOW_SIZE)
BACKGROUND.fill("Black")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(500,500))

G = 10

class Body(pygame.sprite.Sprite):

    def __init__(self, mass, radius, start_position, color, x_vel, y_vel):
        super().__init__()

        self.image = pygame.Surface((radius*2, radius*2))
        self.image.fill("black")
        self.rect = self.image.get_rect(center = start_position)
        pygame.draw.circle(self.image, color, (radius, radius), radius, 0)

        self.mass = mass
        self.radius = radius
        self.x_pos = start_position[0]
        self.y_pos = start_position[1]

        self.x_vel = x_vel
        self.x_acc = 0
        self.y_vel = y_vel
        self.y_acc = 0

    def set_y_vel(self, value):
        self.y_vel = value

    def set_x_vel(self, value):
        self.x_vel = value

    def set_y_acc(self, value):
        self.y_acc = value

    def set_x_acc(self, value):
        self.x_acc = value

    def change_x_pos(self, value):
        self.x_pos += value

    def change_y_pos(self, value):
        self.y_pos += value

    def change_x_vel(self, value):
        self.x_vel += value

    def change_y_vel(self, value):
        self.y_vel += value

    def update_pos(self):
        self.rect.center = (round(self.x_pos), round(self.y_pos))

    def animate(self):
        self.change_x_vel(self.x_acc)
        self.change_y_vel(self.y_acc)

        self.change_x_pos(self.x_vel)
        self.change_y_pos(self.y_vel)

        self.update_pos()

    def gravitate(self, otherbody):
        dx = abs(self.x_pos - otherbody.x_pos)
        dy = abs(self.y_pos - otherbody.y_pos)

        if dx < self.x_pos*2 and dy < self.radius*2:
            pass

        else:
            try:
                r = math.sqrt(dx**2 + dy**2)
                a = G*otherbody.mass/(r**2)
                theta = math.asin(dy/r)

                if self.y_pos > otherbody.y_pos:
                    self.set_y_acc(-math.sin(theta)*a)
                else:
                    self.set_y_acc(math.sin(theta)*a)
                if self.x_pos > otherbody.x_pos:
                    self.set_x_acc(-math.cos(theta)*a)
                else:
                    self.set_x_acc(math.cos(theta)*a)

            except ZeroDivisionError:
                pass

body_group = pygame.sprite.Group()
BODYCOUNT = 10
for i in range(BODYCOUNT):
    #if i == 0:
     #   body_group.add(Body(100, 10, (500,500), "cyan", 0, 0))

    body_group.add(Body(1, 3, (random.randrange(100,900), random.randrange(100,900)), "white", 0, 0))

body_list = list(body_group)
body_pairs = list(itertools.combinations(body_list, 2))



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    WINDOW.blit(BACKGROUND, BACKGROUND_RECT)
    body_group.draw(WINDOW)

    for body, otherbody in body_pairs:
        body.gravitate(otherbody)
        otherbody.gravitate(body)
        body.animate()
        otherbody.animate()

    pygame.display.update()
    CLOCK.tick(60)
