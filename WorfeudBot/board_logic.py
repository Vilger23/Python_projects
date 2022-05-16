class Board():
    def __init__(self, size_):
        self.size = size_
        row = ['_',]*size_
        self.game_state = [r[:] for r in [row]*size_]
        self.game_state[7][7] = 'd'
        self.game_state[7][8] = 'e'
        self.game_state[7][9] = 'a'
        self.game_state[7][10] = 'r'
        self.game_state[7][11] = 'i'
        self.game_state[7][12] = 'e'

        self.game_state[8][12] = 'x'
        self.game_state[9][12] = 'a'
        self.game_state[10][12] = 'm'
        self.game_state[11][12] = 'e'
        self.game_state[12][12] = 'n'

        self.game_state[9][13] = 'h'
        self.game_state[9][14] = 'a'

        self.game_state[10][13] = 'a'
        self.game_state[10][14] = 'g'

        self.game_state[4][10] = 'r'
        self.game_state[5][10] = 'e'
        self.game_state[6][10] = 'p'
        self.game_state[8][10] = 'o'
        self.game_state[9][10] = 'v'
        self.game_state[10][10] = 'e'
        self.game_state[11][10] = 'd'

        self.game_state[11][9] = 'l'
        self.game_state[11][8] = 'u'
        self.game_state[11][7] = 'o'
        self.game_state[11][6] = 'w'

        self.game_state[10][8] = 'q'
        self.game_state[11][8] = 'u'
        self.game_state[12][8] = 'i'
        self.game_state[13][8] = 't'
        self.game_state[14][8] = 's'

        self.game_state[14][8] = 's'
        self.game_state[14][9] = 'a'
        self.game_state[14][10] = 'u'
        self.game_state[14][11] = 'l'
        self.game_state[14][12] = 't'



    def occupied(self, pos_):
        c, r = pos_
        if self.game_state[r][c] == '_':
            return False
        return True

    def get_surrounding_squares(self, pos_):
        c, r = pos_
        edge = range(0, self.size)
        moves = [
            ( 0, 1),
            ( 1, 0),
            ( 0,-1),
            (-1, 0)
            ]
        surrounding_squares = [(c+dc, r+dr) for dr, dc in moves if (c+dc in edge and r+dr in edge)]
        return surrounding_squares

    def get_possible_moves(self):
        possible_moves = []
        for r in range(self.size):
            for c in range(self.size):
                pos = (c, r) 
                if self.occupied(pos):
                    continue
                surrounding_squares = self.get_surrounding_squares(pos) 
                if any(self.occupied(square) for square in surrounding_squares):
                    possible_moves.append(pos)
        return possible_moves

    def get_line(self, l, i):
        line = []
        for letter in l[i:]:
            if letter != '_':
                line.append(letter)
            else:
                break
        for letter in l[:i][::-1]:
            if letter != '_':
                line.insert(0, letter)
            else:
                break
        return line

        

    def get_words(self, pos_, letter = None):
        c, r = pos_
        if letter:
            self.game_state[r][c] = letter
        row = self.game_state[r]
        horisontal = ''.join(self.get_line(row, c))
        col = [row[c] for row in self.game_state]
        vertical = ''.join(self.get_line(col, r))
        if letter:
            self.game_state[r][c] = '_'

        return (horisontal, vertical)