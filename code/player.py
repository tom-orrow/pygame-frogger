import pygame
import sys
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)

        self.import_assets()
        self.frame_index = 0
        self.status = "down"
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 200

        # collisions
        self.colliion_sprites = collision_sprites

    def collision(self, direction):
        for sprite in self.colliion_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if hasattr(sprite, "name") and sprite.name == "car":
                    pygame.quit()
                    sys.exit()

                if direction == "horizontal":
                    if self.direction.x > 0:  # moving right
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.centerx
                    if self.direction.x < 0:  # moving left
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.centerx
                else:
                    if self.direction.y > 0:  # moving down
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.centery
                    if self.direction.y < 0:  # moving up
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.centery

    def import_assets(self):
        self.animations = {}
        for index, folder in enumerate(walk("../graphics/player")):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in folder[2]:
                    key = folder[0].split("/")[-1]
                    path = folder[0] + "/" + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    self.animations[key].append(surf)

    def move(self, dt):
        # normalize vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # horizontal movement + collision
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        self.collision("horizontal")

        # vertical movement + collision
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = round(self.pos.y)
        self.collision("vertical")

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

    def animate(self, dt):
        current_animation = self.animations[self.status]
        if self.direction.magnitude() != 0:
            self.frame_index += 10 * dt
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
