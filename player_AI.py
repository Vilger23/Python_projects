from itertools import permutations
import copy
from setup import *

class AI():
    def __init__(self, hand_, board_, word_list_):
        self.hand = hand_
        self.board = board_
        self.word_list = word_list_
        self.moves = [
            ( 0, 1),
            ( 1, 0),
            ( 0,-1),
            (-1, 0)
            ]


        return
    def recursive(self, perms, string_):
        if not string_:
            return perms
        perms.update(''.join(a) for a in permutations(string_) )

        for i, let in enumerate(string_):
            self.recursive(perms, string_[:i] + string_[i+1:])
        return perms
        

    def find_best_move(self):
        actual_moves = []
        possible_moves = self.board.get_possible_moves()
        permu = list( self.recursive(set(), ''.join(self.hand)) )
        for i, word in enumerate(permu):
            if i%10 == 0:
                print(round(i/len(permu)*100, 4))
            found = False
            for w in word_list:
                i= -1
                y = 0
                while True:
                   
                    wo = w[i+1:]
                    i = wo.find(word[y]) 
                    y+=1
                    if y == len(word):
                        found = True
                        break
                    if i == -1:
                        break
                if found:
                    break
            else:
                continue

            for r in range(self.board.size):
                for c in range(self.board.size):
                    og = copy.deepcopy(self.board.game_state)
                    for dc, dr in [(1,0), (0,1)]:
                        tc = c
                        tr = r
                        positions = []
                        i = 0
                        while not (i == len(word) or tc == self.board.size or tr == self.board.size):

                            if self.board.occupied( (tc,tr) ):
                                tc += dc
                                tr += dr
                            else:
                                self.board.game_state[tr][tc] = word[i]
                                positions.append( (tc,tr) )
                                i += 1
                        if len(positions) != len(word):      
                            self.board.game_state = copy.deepcopy(og)
                            continue
                        segments = []


                        for pos in positions:
                            segments.append(self.board.get_words(pos)[dc])
                        segments.append(self.board.get_words(positions[0])[dr])

                        segments = [seg for seg in segments if seg != '_' and len(seg)!= 1]

                        if not segments:
                            self.board.game_state = copy.deepcopy(og)
                            continue

                        if not any(seg.upper() not in self.word_list for seg in segments) and any(pos in possible_moves for pos in positions):
                            actual_moves.append( (segments, positions))
                        self.board.game_state = copy.deepcopy(og)

        actual_moves.sort(key = lambda x:sum( [points[let.upper()] for word in x[0] for let in word] ), reverse = True)
        return actual_moves


                        





                





