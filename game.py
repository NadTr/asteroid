from if3_game.engine import Sprite, Layer, Text, Game
from pyglet.window import key
from math import cos, sin, radians
from random import randint

RESOLUTION = [1200,800]
CENTER = [RESOLUTION[0]/2, RESOLUTION[1]/2]

class AsteroidGame(Game):
    def __init__(self):   
        super().__init__()
        self.asteroids = []
        self.points = []

        self.game_backround = Layer()
        self.game_backround.add(Sprite("images/galaxy2.jpg", CENTER, anchor=(800,800)))

        self.game_layer = Layer()
        self.spaceship = Spaceship(CENTER)
        # self.game_layer.add(self.spaceship)

        self.ui_layer = UILayer(self.spaceship)
        # self.game_layer.add(ast1, ast2, ast3)
        self.add(self.game_backround, self.game_layer, self.ui_layer)

        self.initialize()       

    def initialize(self):

        for asteroid in self.asteroids:
            asteroid.level = 1
            asteroid.destroy()

        self.spaceship.destroy()
        self.asteroids = []  

        self.spaceship = Spaceship(CENTER)
        self.game_layer.add(self.spaceship)

        self.ui_layer.spaceship = self.spaceship

        self.asteroids.append(Asteroid((500,150), [80, 0], 150))
        self.asteroids.append(Asteroid((150,100), [20, 50], -80))
        self.asteroids.append(Asteroid((300,650), [45, 15], 20)) 

        for asteroid in self.asteroids:
            self.game_layer.add(asteroid)

        self.points = []
    
    def showpoints(self):
        return sum(self.points)
            


class UILayer(Layer):
    def __init__(self, ship):
        super().__init__()
        self.points = 0
        self.spaceship = ship
        self.life_sprites = []
        life_position = (20, RESOLUTION[1] - 15)

        self.game_over = Sprite("images/game_over.png",CENTER, anchor=(300, 178))
        self.game_over.opacity = 0
        self.add(self.game_over)

        for n in range(0, self.spaceship.hp):
            x, y = life_position
            x += n * 20
            life_sprite = Sprite("images/life.png", (x, y), anchor=(8,8))
            self.add(life_sprite)
            self.life_sprites.append(life_sprite)

        self.points_text = Text(f"Points: {self.points}", (RESOLUTION[0]-125, RESOLUTION[1]-30), 20)
        self.add(self.points_text)

    def update(self, dt):
        super().update(dt)
        self.points = self.game.showpoints()
        self.points_text.text = f"Points: {self.points}"
        for n, life_sprite in enumerate(self.life_sprites):   
            if n < self.spaceship.hp:
                life_sprite.opacity = 255
            else : 
                life_sprite.opacity = 0
        if self.spaceship.hp <= 0:
            # game_over = Text("Game Over", CENTER, 120, color = (0, 0, 0, 255), anchor = "center")
            # game_over = Sprite("images/game_over.png",CENTER, anchor=(300, 178))
            # self.add(game_over)
            self.game_over.opacity = 255

    def on_key_press(self, k, modifiers):
        super().on_key_press(k, modifiers)
        if self.spaceship.hp < 1 and k == key.ENTER:
            self.game_over.opacity = 0

            self.game.initialize()
             



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
    def __init__(self, position, initial_speed, initial_rotation_speed, level = 3):
        self.rotation_speed = initial_rotation_speed

        stats = {
            3:  {
                "image" : "images/ast_big.png",
                "anchor" : (50,47),
                },
            2:  {
                "image" : "images/ast_middle.png",
                "anchor" : (30,27),
                },
            1:  {
                "image" : "images/ast_little.png",
                "anchor" : (8,7),
                },
        }
        self.level = level
        image = stats[self.level]['image']
        anchor = stats[self.level]['anchor']
        super().__init__(image, position, anchor, initial_speed) 

    def update(self, delta_time):
        super().update(delta_time)
        self.rotation += self.rotation_speed * delta_time

    def spawn_children(self):
        for x in range(0, 3):
            # rotation = x * 360/number_children
            # angle = radians(rotation)
            # ast_speed_x = 30 * cos(angle)
            # ast_speed_y = -30 * sin (angle)
            level = self.level - 1
            rotation = randint(-100, 100)
            ast_speed_x = randint(-30, 30)
            ast_speed_y = randint(-30, 30)
            ast_speed = ast_speed_x, ast_speed_y
            asteroid = Asteroid(self.position, ast_speed, rotation, level)
            self.layer.add(asteroid)
            self.layer.game.asteroids.append(asteroid)
            # self.layer.game.points += 1
            
    def destroy(self):
        super().destroy()
        if self.level <= 1:
            self.layer.game.points.append(1)
            return

        self.spawn_children()

    def on_collision(self, other):
        super().on_collision(other)
        if isinstance(other,Spaceship):
            other.destroy()

        if isinstance(other,Bullet):
            other.destroy()
            self.destroy()


class Spaceship(SpaceElement):
    def __init__(self, position):
        super().__init__("images/spaceship.png", position, (32,32), [0,0]) 
        self.hp = 3
        self.point = 0
        self.rotated = 45
        self.rotation_speed = 0
        self.turning_speed = 90
        self.acceleration = 0
        self.speed_intensity = 0
        self.shooting = 0
        self.cooldown = 0.0
        self.invicible = 0.0

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
        self.speed_intensity = max(0, self.speed_intensity)
        angle = radians(self.rotation - self.rotated)
        speed_x = self.speed_intensity * cos(angle) 
        speed_y = -self.speed_intensity * sin(angle) 
        self.speed = speed_x, speed_y
        if self.shooting and self.cooldown <= 0:
            self.shoot()
            self.cooldown = 0.25
        elif self.shooting: 
            self.cooldown -= delta_time

        if self.invicible > 0:
            self.invicible -= delta_time
            self.opacity = 125
        else:
            self.opacity = 255


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

    def destroy(self):
        if self.invicible <= 0:
            self.hp -= 1
            self.invicible = 3.0
        else:
            if self.hp <= 0:
                super().destroy()



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
