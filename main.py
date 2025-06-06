from if3_game.engine import init
from game import  RESOLUTION, AsteroidGame

title = "Asteroid"
init(RESOLUTION, title)
# game_backround = Layer()
# backround_img = Sprite("images/galaxy2.jpg", CENTER, anchor=(800,800))
# game_backround.add(backround_img)


# ast1 = Asteroid((500,150), [80, 0], 150)
# ast2 = Asteroid((150,100), [20, 50], -80)
# ast3 = Asteroid((300,650), [45, 15], 20)
# spaceship = Spaceship(CENTER)

# ui_layer = UILayer(spaceship)
# game_layer = Layer()
# game = Game()
# # text = Text()
# game_layer.add(ast1, ast2, ast3)
# game_layer.add(spaceship)
# game.add(game_backround)
# game.add(ui_layer)
# game.add(game_layer)
# game.debug = True #affiche les formes de collision
game = AsteroidGame()
game.run()