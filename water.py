import pygame
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

water_color = (41, 179, 174)
ice_color = (184, 217, 216)
# change color; using hsv would be easier
# change based on y (controlled by waterLane; color) and x (distance from center; darkness)
ice_num = 4
section_width = SCREEN_WIDTH//(ice_num-1)
grid = 40


class WaterLane(pygame.sprite.Sprite):

    def __init__(self, y, velocity):
        super().__init__()
        self.velocity = velocity
        self.ice_list = pygame.sprite.Group()
        self.temp_list = []
        self.rect = pygame.Rect(0, y, SCREEN_WIDTH, grid)
        self.get_ice()

    def get_ice(self):
        for i in range(ice_num):
            width = random.randint(grid, section_width-grid//2)
            new_ice = Ice(section_width*i, self.rect.y, self.velocity, width)
            self.ice_list.add(new_ice)
            self.temp_list.append(new_ice)


class Ice(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, width):
        super().__init__()
        self.velocity = velocity
        self.width = width
        self.image = pygame.Surface((width, grid*6//7))
        self.image.fill(ice_color)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    # moves ice blocks and loops them back to the beginning once they reach the end of the screen
    def ice_animation(self):
        self.rect.x += self.velocity
        if self.rect.x < -section_width:
            self.rect.x = SCREEN_WIDTH
        if self.rect.x > SCREEN_WIDTH:
            self.rect.x = -section_width

    def update(self, current_y):
        self.rect.y = current_y
        self.ice_animation()


