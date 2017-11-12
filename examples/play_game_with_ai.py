from random_ai import RandomAI # Import Your AI
from connect6 import Game

a = RandomAI()
b = RandomAI()
game = Game(AI1 = a, AI2 = None)
game.start_game_gui()
