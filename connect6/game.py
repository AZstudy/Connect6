import pyglet
from pyglet import clock

import os 
import numpy as np

from . import AIAbstractClass


class Game():
    def __init__(self, AI1=None, AI2=None, states = None):
        # MACRO
        RES_PATH = "res/"
        SIZE  = 9
        BOARD = "board9.png"
        BLACK = "black80.png"
        WHITE = "white80.png"
        MARGIN = 45
        GRID_SIZE = 80
        
        # State MACRO
        self.EMPTY_STATE = 0
        self.BLACK_STATE = 1
        self.WHITE_STATE = 2

        self.BLACKS_TURN = 0
        self.WHITES_TURN = 1

        self.BLACK_WINS = 0
        self.WHITE_WINS = 1
        self.IN_PROGRESS = 2

        # Settings
        self.board_size = SIZE
        self.board_path = RES_PATH + BOARD
        self.black_path = RES_PATH + BLACK
        self.white_path = RES_PATH + WHITE
        self.margin =     MARGIN
        self.grid_size =  GRID_SIZE

        # GUI
        self.window = None
        self.board = None
        self.black_stone = None
        self.white_stone = None
        self.gui_mode = None

        # Game
        self.turn = None
        self.left_turn = None
        self.game_state = None
        self.board_state = None

        # Async
        self.loop = None

        # AI
        self.AI1 = AI1
        self.AI2 = AI2
        assert(AI1 == None or isinstance(AI1, AIAbstractClass))
        assert(AI2 == None or isinstance(AI2, AIAbstractClass))

        # States
        self.gui_mode = False
        self.clear_board()
        if states != None:
            self.init_with_states(states)
        self.gui_mode = False

    def start_game_gui(self):
        self.gui_mode = True
        self.clear_board()
        self.play_game()
        pyglet.app.run()

    def start_game_without_gui(self):
        self.gui_mode = False
        self.clear_board()

    def play_game(self):
        if self.AI1 != None and self.turn == self.BLACKS_TURN:
            x, y = self.AI1.action(self.states())
            self.run_action(x, y)
        elif self.AI2 != None and self.turn == self.WHITES_TURN:
            x, y = self.AI2.action(self.states())
            self.run_action(x, y)
        else:
            # Wait for User to play
            pass

    def states(self):
        turn, left_turn, board_state, game_state = self.turn, self.left_turn, self.board_state, self.game_state

        return (board_state, left_turn, turn, game_state)

    def init_with_states(self, states):
        self.gui_mode = False
        self.clear_board()

        (self.board_state, self.left_turn, self.turn, self.game_state) = states

    def run_action(self,x, y):
        if self.board_state[x][y] != self.EMPTY_STATE:
            return self.states()
        if self.game_state != self.IN_PROGRESS:
            return self.states()

        if self.turn == self.BLACKS_TURN:
            self.board_state[x][y] = self.BLACK_STATE
        else:
            self.board_state[x][y] = self.WHITE_STATE

        if self.left_turn == 1: 
            self.left_turn = 2
            self.turn = self.BLACKS_TURN + self.WHITES_TURN - self.turn
        else:
            self.left_turn = self.left_turn - 1

        self.game_state = self.is_terminated()
        if self.gui_mode == True: self.render()

        return self.states()

    def is_possible_action(self,x,y):
        if (self.board_state[x][y] == self.EMPTY_STATE): return True
        else: return False

    def reset_game(self):
        self.clear_board()

    def clear_board(self):
        self.board_state = np.full((9, 9), self.EMPTY_STATE)
        self.turn = self.BLACKS_TURN
        self.left_turn = 1
        self.game_state = self.IN_PROGRESS

        if self.window == None and self.gui_mode == True:
            self.init_window()

    def is_terminated(self):
        horiz = [{'cnt_b': 0, 'cnt_w': 0, 'max_b': 0, 'max_w': 0} for i in range(self.board_size)]
        verti = [{'cnt_b': 0, 'cnt_w': 0, 'max_b': 0, 'max_w': 0} for i in range(self.board_size)]
        diag1 = [{'cnt_b': 0, 'cnt_w': 0, 'max_b': 0, 'max_w': 0} for i in range(self.board_size*2)]
        diag2 = [{'cnt_b': 0, 'cnt_w': 0, 'max_b': 0, 'max_w': 0} for i in range(self.board_size*2)]

        for i, row in enumerate(self.board_state):
            for j, s in enumerate(row):
                h, v, d1, d2 = horiz[i], verti[j], diag1[i+j], diag2[i-j+8]
                # Save to max
                if (s == self.EMPTY_STATE or self.BLACK_STATE):
                    if h['cnt_w'] > h['max_w']: h['max_w'] = h['cnt_w']
                    if v['cnt_w'] > v['max_w']: v['max_w'] = v['cnt_w']
                    if d1['cnt_w'] > d1['max_w']: d1['max_w'] = d1['cnt_w']
                    if d2['cnt_w'] > d2['max_w']: d2['max_w'] = d2['cnt_w']
                if (s == self.EMPTY_STATE or self.WHITE_STATE):
                    if h['cnt_b'] > h['max_b']: h['max_b'] = h['cnt_b']
                    if v['cnt_b'] > v['max_b']: v['max_b'] = v['cnt_b']
                    if d1['cnt_b'] > d1['max_b']: d1['max_b'] = d1['cnt_b']
                    if d2['cnt_b'] > d2['max_b']: d2['max_b'] = d2['cnt_b']

                # Reset or Update
                if (s == self.EMPTY_STATE):
                    h['cnt_b'], h['cnt_w'] = 0, 0
                    v['cnt_b'], v['cnt_w'] = 0, 0
                    d1['cnt_b'], d1['cnt_w'] = 0, 0
                    d2['cnt_b'], d2['cnt_w'] = 0, 0
                elif(s == self.BLACK_STATE):
                    h['cnt_b'], h['cnt_w'] = h['cnt_b']+1, 0
                    v['cnt_b'], v['cnt_w'] = v['cnt_b']+1, 0
                    d1['cnt_b'], d1['cnt_w'] = d1['cnt_b']+1, 0
                    d2['cnt_b'], d2['cnt_w'] = d2['cnt_b']+1, 0
                elif(s == self.WHITE_STATE):
                    h['cnt_b'], h['cnt_w'] = 0, h['cnt_w']+1
                    v['cnt_b'], v['cnt_w'] = 0, v['cnt_w']+1
                    d1['cnt_b'], d1['cnt_w'] = 0, d1['cnt_w']+1
                    d2['cnt_b'], d2['cnt_w'] = 0, d2['cnt_w']+1

        max_b = max([c for data in [horiz, verti, diag1, diag2] for x in data for c in [x['max_b'], x['cnt_b']]])
        max_w = max([c for data in [horiz, verti, diag1, diag2] for x in data for c in [x['max_w'], x['cnt_w']]])

        if max_b == 6: return self.BLACK_WINS
        elif max_w == 6: return self.WHITE_WINS
        else: return self.IN_PROGRESS


    def init_window(self):
        script_dir = os.path.dirname(__file__)
        self.board = pyglet.image.load(os.path.join(script_dir, self.board_path))
        self.black_stone = pyglet.image.load(os.path.join(script_dir, self.black_path)) 
        self.white_stone = pyglet.image.load(os.path.join(script_dir, self.white_path))

        self.window = pyglet.window.Window(self.board.width, self.board.height)
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        self.set_events()

        # Label
        self.black_wins = pyglet.text.Label('Black Player Wins!',
                      font_name='Times New Roman',
                      font_size=36,
                      color=(125, 125, 125, 255),
                      x=self.window.width//2, y=self.window.height//2,
                      anchor_x='center', anchor_y='center')
        self.white_wins = pyglet.text.Label('White Player Wins!',
                      font_name='Times New Roman',
                      font_size=36,
                      color=(125, 125, 125, 255),
                      x=self.window.width//2, y=self.window.height//2,
                      anchor_x='center', anchor_y='center')

    def set_events(self):
        @self.window.event
        def on_draw():
            self.render()

        @self.window.event
        def on_mouse_release(x, y, button, modifiers):
            if self.game_state != self.IN_PROGRESS:
                self.window.close()
                return

            if self.AI1 != None and self.turn == self.BLACKS_TURN: return
            if self.AI2 != None and self.turn == self.WHITES_TURN: return

            x = int((x - self.margin)/self.grid_size + 0.5)
            y = int((y - self.margin)/self.grid_size + 0.5)

            x, y = 8-y, x

            if x < 0: x = 0 
            elif x > 8: x = 8

            if y < 0 : y = 0
            elif y > 8: y= 0
            
            self.run_action(x, y)

        def callback(dt):
            self.play_game()
        clock.schedule_interval(callback, .5)

    def render(self):
        self.window.clear()
        self.board.blit(0,0)
        it = np.nditer(self.board_state, flags=['multi_index'])
        while not it.finished:
            grid = it.multi_index
            if it[0] == self.WHITE_STATE:
                self.sprites.append(pyglet.sprite.Sprite(self.white_stone,x = self.margin + self.grid_size * grid[1] - self.grid_size/2, y = self.margin + self.grid_size*(8-grid[0]) - self.grid_size/2, batch= self.batch))
            elif it[0] == self.BLACK_STATE:
                self.sprites.append(pyglet.sprite.Sprite(self.black_stone, x = self.margin + self.grid_size * grid[1] - self.grid_size/2, y = self.margin + self.grid_size*(8-grid[0])-self.grid_size/2, batch= self.batch))
            else: pass

            it.iternext()
        self.batch.draw()

        # Winning label
        if self.game_state == self.BLACK_WINS: self.black_wins.draw()
        if self.game_state == self.WHITE_WINS: self.white_wins.draw()
