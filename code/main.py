import sys
import pygame

from player import Player
from car import Car
from sprite import SimpleSprite
from sprite import LongSprite
from settings import *
from random import choice, randint


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.bg = pygame.image.load("../graphics/main/map.png").convert()
        self.fg = pygame.image.load("../graphics/main/overlay.png").convert_alpha()

    def customize_draw(self):
        # change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # blit bg
        display_surface.blit(self.bg, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)

        # blit fg
        display_surface.blit(self.fg, -self.offset)


pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()

# groups
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

# sprites
player = Player((2062, 3274), all_sprites, obstacle_sprites)


# sprite setup
for file_name, pos_list in SIMPLE_OBJECTS.items():
    path = f"../graphics/objects/simple/{file_name}.png"
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        SimpleSprite(surf, pos, [all_sprites, obstacle_sprites])

for file_name, pos_list in LONG_OBJECTS.items():
    path = f"../graphics/objects/long/{file_name}.png"
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        LongSprite(surf, pos, [all_sprites, obstacle_sprites])

# timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 50)
pos_list = []

# game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == car_timer:
            random_pos = choice(CAR_START_POSITIONS)
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                pos = (random_pos[0], random_pos[1] + randint(-8, 8))
                Car(pos, [all_sprites, obstacle_sprites])
            if len(pos_list) > 5:
                del pos_list[0]

    # delta time
    dt = clock.tick() / 1000

    # draw bg
    display_surface.fill("black")

    # draw
    # all_sprites.draw(display_surface)
    all_sprites.customize_draw()

    # update
    all_sprites.update(dt)

    # final frame
    pygame.display.update()
