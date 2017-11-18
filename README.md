# Connect6
Connect6 Environment for Reinforcement Learning

# Installation
```
pip3 install -e .
```

# Examples
```
python3 examples/start_game_with_gui.py
python3 examples/play_game_with_ai.py
```

# States
```
game = Game()
state = game.states() 
```

state : (board_state, left_turn, turn, game_state)
    board_state : 9 by 9 python array (0 : Empty, 1 : Black stone, 2 : White stone)
    left_turn : number of turn left
    turn : (0 : Black's turn, 1 : White's turn)
    game_state : (0 : Black win, 1: White win, 2: In progress)
