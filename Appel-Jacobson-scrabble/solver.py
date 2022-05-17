from letter_tree import basic_language
from board import sample_board
import operator
def prod(factors):
    product = 1
    for p in factors:
        product *= p
    return product


letters =       ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
letter_points = [1  ,   3,   3,   2,   1,   4,   2,   4,   1,   8,   5,   1,   3,   1,   1,   3,   10,   1,   1,   1,   1,   4,   4,   8,   4, 10]

sv_points = {1: ['a','d','e','i','n','r','s','t' ], 2: ['g','l','o'], 3: ['b','f','h','k','m','v'], 4: ['p','u','å','ä','ä'], 7: ['j', 'y'], 8: ['c', 'x', 'z']}

class SolveState:
    legal_moves = []
    def __init__(self, dictionary, board, language, rack):
        self.dictionary = dictionary
        self.board = board
        self.rack = [letter for letter in rack]
        self.cross_check_results = None
        self.direction = None

        if language == 'en': 
            self.points = {letter.lower():point for letter, point in zip(letters,letter_points)}
            self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        if language == 'sv': 
            self.points = { letter.lower():point for point in [1,2,3,4,7,8] for letter in sv_points[point] }
            self.alphabet = 'abcdefghijklmnopqrstuvxyzåäö'



        self.letter_converter = {'tb': 3, 'db':2, 'to':1, 'do':1, '..':1}
        self.word_converter = {'tb': 1, 'db':1, 'to':3, 'do':2, '..':1}
        self.multiplier_overlay = [
            ['tb', '..', '..', '..', 'to', '..', '..', 'db', '..', '..', 'to', '..', '..', '..', 'tb'],
            ['..', 'db', '..', '..', '..', 'tb', '..', '..', '..', 'tb', '..', '..', '..', 'db', '..'],
            ['..', '..', 'do', '..', '..', '..', 'db', '..', 'db', '..', '..', '..', 'do', '..', '..'],
            ['..', '..', '..', 'tb', '..', '..', '..', 'do', '..', '..', '..', 'tb', '..', '..', '..'],
            ['to', '..', '..', '..', 'do', '..', 'db', '..', 'db', '..', 'do', '..', '..', '..', 'to'],
            ['..', 'tb', '..', '..', '..', 'tb', '..', '..', '..', 'tb', '..', '..', '..', 'tb', '..'],
            ['..', '..', 'db', '..', 'db', '..', '..', '..', '..', '..', 'db', '..', 'db', '..', '..'],
            ['db', '..', '..', 'do', '..', '..', '..', '..', '..', '..', '..', 'do', '..', '..', 'db'],
            ['..', '..', 'db', '..', 'db', '..', '..', '..', '..', '..', 'db', '..', 'db', '..', '..'],
            ['..', 'tb', '..', '..', '..', 'tb', '..', '..', '..', 'tb', '..', '..', '..', 'tb', '..'],
            ['to', '..', '..', '..', 'do', '..', 'db', '..', 'db', '..', 'do', '..', '..', '..', 'to'],
            ['..', '..', '..', 'tb', '..', '..', '..', 'do', '..', '..', '..', 'tb', '..', '..', '..'],
            ['..', '..', 'do', '..', '..', '..', 'db', '..', 'db', '..', '..', '..', 'do', '..', '..'],
            ['..', 'db', '..', '..', '..', 'tb', '..', '..', '..', 'tb', '..', '..', '..', 'db', '..'],
            ['tb', '..', '..', '..', 'to', '..', '..', 'db', '..', '..', 'to', '..', '..', '..', 'tb']
        ]

    def before(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row, col - 1
        else:
            return row - 1, col

    def after(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row, col + 1
        else:
            return row + 1, col

    def before_cross(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row - 1, col
        else:
            return row, col - 1

    def after_cross(self, pos):
        row, col = pos
        if self.direction == 'across':
            return row + 1, col
        else:
            return row, col + 1

    def calculate_points(self, every_pos, plays, word):
        curr_points = 0
        final_points = 0
        for play in plays:
            pos, letter = play
            r, c = pos
            buffed = self.points[letter]*self.letter_converter[self.multiplier_overlay[r][c]]
            final_points += buffed
            cross = ''.join(self.cross_word(pos))
            if cross:
                curr_points += (buffed + sum( self.points[l] for l in cross ))*self.word_converter[self.multiplier_overlay[r][c]]

        for play in every_pos:
            if play not in [p[0] for p in plays]:
                final_points += self.points[self.board.get_tile(play)]
        final_points *= prod(self.word_converter[self.multiplier_overlay[r][c]] for (r, c), letter in plays)

        if len(plays) == 7:
            final_points += 40
        return curr_points + final_points


    def legal_move(self, word, last_pos):
        board_if_we_played_that = self.board.copy()

        play_pos = last_pos
        every_pos = []
        word_idx = len(word) - 1
        legals = []

        while word_idx >= 0:

            board_if_we_played_that.set_tile(play_pos, word[word_idx].upper())
            if not self.board.is_filled(play_pos):
                legals.append( (play_pos, word[word_idx]) )
            every_pos.append(play_pos)

            word_idx -= 1
            play_pos = self.before(play_pos)
        self.legal_moves.append((self.calculate_points(every_pos, legals, word), board_if_we_played_that))

    def cross_word(self, pos):
        letters_before = ""
        scan_pos = pos
        while self.board.is_filled(self.before_cross(scan_pos)):
            scan_pos = self.before_cross(scan_pos)
            letters_before = self.board.get_tile(scan_pos) + letters_before
        letters_after = ""
        scan_pos = pos
        while self.board.is_filled(self.after_cross(scan_pos)):
            scan_pos = self.after_cross(scan_pos)
            letters_after = letters_after + self.board.get_tile(scan_pos)
        return letters_before, letters_after


    def cross_check(self):
        result = dict()
        for pos in self.board.all_positions():
            if self.board.is_filled(pos):
                continue
            letters_before, letters_after = self.cross_word(pos)

            if len(letters_before) == 0 and len(letters_after) == 0:
                legal_here = list(self.alphabet)
            else:
                legal_here = []
                for letter in self.alphabet:
                    word_formed = letters_before + letter + letters_after
                    if self.dictionary.is_word(word_formed):
                        legal_here.append(letter)
            result[pos] = legal_here
        return result

    def find_anchors(self):
        anchors = []
        for pos in self.board.all_positions():
            empty = self.board.is_empty(pos)
            neighbor_filled = self.board.is_filled(self.before(pos)) or \
                              self.board.is_filled(self.after(pos)) or \
                              self.board.is_filled(self.before_cross(pos)) or \
                              self.board.is_filled(self.after_cross(pos))
            if empty and neighbor_filled:
                anchors.append(pos)
        return anchors

    def before_part(self, partial_word, current_node, anchor_pos, limit):
        self.extend_after(partial_word, current_node, anchor_pos, False)
        if limit > 0:
            for next_letter in current_node.children.keys():
                if next_letter in self.rack:
                    self.rack.remove(next_letter)
                    self.before_part(
                        partial_word + next_letter,
                        current_node.children[next_letter],
                        anchor_pos,
                        limit - 1
                    )
                    self.rack.append(next_letter)

    def extend_after(self, partial_word, current_node, next_pos, anchor_filled):
        if not self.board.is_filled(next_pos) and current_node.is_word and anchor_filled:
            self.legal_move(partial_word, self.before(next_pos))
        if self.board.in_bounds(next_pos):
            if self.board.is_empty(next_pos):
                for next_letter in current_node.children.keys():

                    if next_letter in self.rack and next_letter in self.cross_check_results[next_pos]:
                        self.rack.remove(next_letter)
                        self.extend_after(
                            partial_word + next_letter,
                            current_node.children[next_letter],
                            self.after(next_pos),
                            True
                        )
                        self.rack.append(next_letter)
            else:
                existing_letter = self.board.get_tile(next_pos)
                if existing_letter in current_node.children.keys():
                    self.extend_after(
                        partial_word + existing_letter,
                        current_node.children[existing_letter],
                        self.after(next_pos),
                        True
                    )

    def find_all_options(self):
        for direction in ['across', 'down']:
            self.direction = direction
            anchors = self.find_anchors()
            self.cross_check_results = self.cross_check()
            for anchor_pos in anchors:
                if self.board.is_filled(self.before(anchor_pos)):
                    scan_pos = self.before(anchor_pos)
                    partial_word = self.board.get_tile(scan_pos)
                    while self.board.is_filled(self.before(scan_pos)):
                        scan_pos = self.before(scan_pos)
                        partial_word = self.board.get_tile(scan_pos) + partial_word
                    pw_node = self.dictionary.lookup(partial_word)
                    if pw_node is not None:
                        self.extend_after(
                            partial_word,
                            pw_node,
                            anchor_pos,
                            False
                        )
                else:
                    limit = 0
                    scan_pos = anchor_pos
                    while self.board.is_empty(self.before(scan_pos)) and self.before(scan_pos) not in anchors:
                        limit = limit + 1
                        scan_pos = self.before(scan_pos)
                    self.before_part("", self.dictionary.root, anchor_pos, limit)



language = 'sv'
rack = 'vuunaäe'
solver = SolveState(basic_language(language), sample_board(), language, rack)
print(solver.board)
print()
solver.find_all_options()
SolveState.legal_moves.sort(key = lambda x:x[0], reverse = True)
for i in range(3):
    print(SolveState.legal_moves[i][0])
    print(SolveState.legal_moves[i][1])