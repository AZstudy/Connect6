from random_ai import RandomAI # Import Your AI
from zero_ai import ZeroAI
from connect6 import Game

a = RandomAI()
b = RandomAI()
game = Game(AI1 = a, AI2 = b)
game.start_game_gui()
