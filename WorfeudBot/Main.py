from setup import *
from board_logic import Board
from player_AI import AI
b = Board(15)
hand_ = 'ikeavfd'
hand_ = [l for l in hand_]
player = AI(hand_, b, word_list)

pos = (8, 5)
surrounding_squares = b.get_surrounding_squares(pos) 
print(player.find_best_move())