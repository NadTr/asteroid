from if3_game.engine import Sprite
from pyglet.window import key
from math import cos, sin, radians
from random import randint

RESOLUTION = [800,600]
CENTER = [RESOLUTION[0]/2, RESOLUTION[1]/2]

class SpaceElement(Sprite):
    def __init__(self, image, position, image_anchor, initial_speed=[0, 0], ):
        super().__init__(image, position, anchor=image_anchor, collision_shape="circle") 
        self.speed = initial_speed

    def update(self, delta_time):
        super().update(delta_time)
        x, y = self.position
        speed_x, speed_y = self.speed
        x += speed_x * delta_time
        y += speed_y * delta_time

        rect = self.get_rect()
        if rect.left > RESOLUTION[0]:
            x = -self.anchor[0]
        elif rect.right < 0:
            x = RESOLUTION[0] + self.anchor[0]

        if rect.bottom > RESOLUTION[1]:
            y = -self.anchor[1]
        elif rect.top < 0:
            y = RESOLUTION[1] + self.anchor[1]

        self.position = x, y


class Asteroid(SpaceElement):
    def __init__(self, image, position, anchor, initial_speed, initial_rotation_speed):
        super().__init__(image, position, anchor, initial_speed) 
        self.rotation_speed = initial_rotation_speed

    def update(self, delta_time):
        super().update(delta_time)
        self.rotation += self.rotation_speed * delta_time

    def spawn_children(self, number_children, type_chidren):
        for x in range(0, number_children):
            rotation = x * 360/number_children
            angle = radians(rotation)
            ast_speed_x = 30 * cos(angle)
            ast_speed_y = -30 * sin (angle)
            # rotation = randint(-100, 100)
            # ast_speed_x = randint(-10, 10)
            # ast_speed_y = randint(-10, 10)
            ast_speed = ast_speed_x, ast_speed_y
            if type_chidren == "middle":
                self.layer.add(MiddleAsteroid(self.position, ast_speed, rotation))
            else : 
                self.layer.add(LittleAsteroid(self.position, ast_speed, rotation))
            
    def destroy(self):
        super().destroy()
        if isinstance(self, BigAsteroid):
            self.spawn_children(3, "middle")
        elif isinstance(self, MiddleAsteroid):
            self.spawn_children(4, "little")

    def on_collision(self, other):
        super().on_collision(other)
        if isinstance(other,Spaceship):
            other.destroy()

        if isinstance(other,Bullet):
            other.destroy()
            self.destroy()


class BigAsteroid(Asteroid, SpaceElement):
    def __init__(self, position, initial_speed, initial_rotation_speed):
        super().__init__("images/ast_big.png", position, (50,47), initial_speed, initial_rotation_speed) 


class MiddleAsteroid(Asteroid, SpaceElement):
    def __init__(self, position, initial_speed, initial_rotation_speed):
        super().__init__("images/ast_middle.png", position, (30,27), initial_speed, initial_rotation_speed) 


class LittleAsteroid(Asteroid, SpaceElement):
    def __init__(self, position, initial_speed, initial_rotation_speed):
        super().__init__("images/ast_little.png", position, (8,7), initial_speed, initial_rotation_speed) 


class Spaceship(SpaceElement):
    def __init__(self, position):
        super().__init__("images/spaceship.png", position, (32,32), [0,0]) 
        self.rotated = 45
        self.rotation_speed = 0
        self.turning_speed = 90
        self.acceleration = 0
        self.speed_intensity = 0
        self.shooting = 0
        self.cooldown = 0

    def shoot(self):
        rotation = self.rotation - self.rotated
        angle = radians(rotation)
        bullet_speed_x = 300 * cos(angle)
        bullet_speed_y = -300 * sin (angle)
        bullet_speed = bullet_speed_x, bullet_speed_y
        bullet = Bullet(self.position, bullet_speed, rotation)
        self.layer.add(bullet)


    def update(self, delta_time):
        speed_x, speed_y = self.speed
        self.speed_intensity += self.acceleration * delta_time
        angle = radians(self.rotation - self.rotated)
        speed_x = self.speed_intensity * cos(angle) 
        speed_y = -self.speed_intensity * sin(angle) 
        self.speed = speed_x, speed_y
        if self.shooting and self.cooldown <= 0:
            self.shoot()
            self.cooldown = 0.25
        elif self.shooting: 
            self.cooldown -= delta_time

        super().update(delta_time)
        self.rotation += self.rotation_speed * delta_time
    
    def on_key_press(self, k, modifier):
        if k == key.RIGHT:
            self.rotation_speed += self.turning_speed
        if k == key.LEFT:
            self.rotation_speed -= self.turning_speed
        if k == key.UP:
            self.acceleration += 100
        if k == key.DOWN:
            # self.acceleration = max(0, self.acceleration - 100)
            self.acceleration -= 100
        if k == key.SPACE:
            self.shooting = True

    def on_key_release(self, k, modifier):
        if k == key.RIGHT:
            self.rotation_speed -= self.turning_speed
        if k == key.LEFT:
            self.rotation_speed += self.turning_speed
        if k == key.UP:
            self.acceleration = 0
        if k == key.DOWN:
            self.acceleration = 0
        if k == key.SPACE:
            self.shooting = False


class Bullet(SpaceElement):
    def __init__(self, position, initial_speed, rotation):
        super().__init__("images/shoot.png", position, (20,14), initial_speed) 
        self.lifetime = 2.0
        self.rotation = rotation
        self.acceleration = 1.01

    def update(self, delta_time):
        super().update(delta_time)
        self.lifetime -= delta_time
        if self.lifetime <= 0:
            self.destroy()
        speed_x, speed_y = self.speed
        speed_x *= self.acceleration 
        speed_y *= self.acceleration 
        self.speed = speed_x, speed_y
