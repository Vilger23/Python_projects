from saved_games import *

class Board:
    def __init__(self, size):
        self.size = size
        self._tiles = ilian_svenska
        self._tiles = [[t if t != ' ' else None for t in row] for row in self._tiles]


    def __str__(self):
        return '\n'.join(' '.join(x if x is not None else '_' for x in row) for row in self._tiles)

    def __sub__(self, other):
        pass

    def all_positions(self):
        result = []
        for row in range(self.size):
            for col in range(self.size):
                result.append((row, col))
        return result

    def get_tile(self, pos):
        row, col = pos
        return self._tiles[row][col]

    def set_tile(self, pos, tile):
        row, col = pos
        self._tiles[row][col] = tile

    def in_bounds(self, pos):
        row, col = pos
        return row >= 0 and row < self.size and col >= 0 and col < self.size

    def is_empty(self, pos):
        return self.in_bounds(pos) and self.get_tile(pos) is None

    def is_filled(self, pos):
        return self.in_bounds(pos) and self.get_tile(pos) is not None

    def copy(self):
        result = Board(self.size)
        for pos in self.all_positions():
            result.set_tile(pos, self.get_tile(pos))
        return result

def sample_board():
    result = Board(15)
    return result
