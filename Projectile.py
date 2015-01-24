from pygame import *

class Projectile():
    def __init__(self, rect, image, velocity):
        self.image = image
        self.rect = rect
        self.velocity = velocity

    def update(self, level):
        self.rect.x+=self.velocity.x
        self.rect.y+=self.velocity.y
        for r in level.platforms:
            if sprite.collide_rect(self, r) and r.solid == True:
                return 5

    def draw(self, surface, camera):
        surface.blit(self.image, Rect(self.rect.x - camera.x, self.rect.y - camera.y, self.rect.width, self.rect.height))