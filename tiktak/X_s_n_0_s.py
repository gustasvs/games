import itertools
import random
import tensorflow

from base_game_spec import BaseGameSpec
from min_max import evaluate

def newBoard():
    return([0, 0, 0],[0, 0, 0],[0, 0, 0])

def apply_move(board_state, move, side):
    move_x, move_y = move
    def get_tuples():
        for x in range(3):
            if move_x == x:
                temp = list(board_state[x])
                temp[move_y] = side
                yield tuple(temp)
            else:
                yield board_state[x]
    return tuple(get_tuples())

def awailableMoves(board_state):
    for x, y in itertools.product(range(3), range(3)):
        if board_state[x][y] == 0:
            yield (x, y)

def ir3(line):
    return all(x == -1for x in line) | all(x == 1 for x in line)

def irWinner(board_state):
    # 0 ja neviens nau
    # 1 ja pirmais
    # -1 j otrais
    for e in range(3):
        if ir3(board_state[e]):
            return board_state[e][0]
    for t in range(3):
        if ir3([i[t] for i in board_state]):
            return board_state[0][t]
    if ir3([board_state[i][i] for i in range(3)]):
        return board_state[0][0]
    if ir3([board_state[2 - i][i] for i in range(3)]):
        return board_state[0][2]
    return 0

def playGame(plusPlayer, minusPlayer, log = False):
    board_state = newBoard()
    player_turn = 1
    while True:
        _awailableMoves = list(awailableMoves(board_state))
        if len(_awailableMoves) == 0:
            #neizskiirts
            if log:
                print("neizskirts")
            return 0
        if player_turn > 0:
            move = plusPlayer(board_state, 1)
        else:
            move = minusPlayer(board_state, -1)

        if move not in _awailableMoves:
            if log:
                print("spiest nemaki?")
            return -player_turn
        board_state = apply_move(board_state, move, player_turn)
        if log:
            print(board_state)
        winner = irWinner(board_state)
        if winner != 0:
            if log:
                print("Winner is: %s" % player_turn)
            return winner
        player_turn = -player_turn

def random_player(board_state, _):
    moves = list(awailableMoves(board_state))
    return random.choice(moves)

class TicTacToe(BaseGameSpec):
    def __init__(self):
        self.awailableMoves = awailableMoves
        self.irWinner = irWinner
        self.newBoard = newBoard
        self.apply_move = apply_move
        self.evaluate = evaluate

    def board_dimensions(self):
        return 3, 3

if __name__ == '__main__':
    playGame(random_player, random_player, log=True)
            

