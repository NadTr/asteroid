from if3_game.engine import init
from game import  RESOLUTION, AsteroidGame

title = "Asteroid"
init(RESOLUTION, title)

# game.debug = True #affiche les formes de collision
game = AsteroidGame()
game.run()