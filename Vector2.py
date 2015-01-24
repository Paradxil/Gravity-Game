import math

class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def rotate(self, angle):
        sin1 = math.sin( angle )
        cos1 = math.cos( angle )
        tx = self.x
        ty = self.y
        nx = (cos1 * tx) - (sin1 * ty)
        ny = (cos1 * ty) + (sin1 * tx)
        return Vector2(nx, ny)