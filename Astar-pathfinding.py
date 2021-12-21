import pygame as pg 
import random
from Colors import *

sqr_nx = 50
sqr_ny = 50
sqr_sz = 15
pad = 1

def one_d(cx, cy):
    index = cx + cy*sqr_nx
    return index

class Cell:
    grid = []
    def __init__(self, _x, _y, _obst = False):
        Cell.grid.append(self)
        self.x = _x
        self.y = _y
        self.sCost = 0
        self.eCost = 0
        self.obst = _obst
        self.parent = None

    def tCost(self):
        return self.eCost + self.sCost

    def get_neighbours(self):
        neighbours = list()
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx = self.x + dx
                ny = self.y + dy

                inborder = (0 <= nx < sqr_nx) and (0 <= ny < sqr_ny)
                if (dx == 0 and dy == 0) or not inborder:
                    continue
                neighbours.append(Cell.grid[one_d(nx, ny)])
        return neighbours

    def grid_dist(a, b):
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        straight = 10 * abs(dx - dy)
        diagonal = 14 * min(dx,  dy)
        return straight + diagonal


def retrace(start, target):
    path = [target]
    curr = target
    while curr != start:
        curr = curr.parent
        path.append(curr)
    return path


def draw(screen, active, visited, path):
    for x in range(sqr_nx):
        for y in range(sqr_ny):
            cell = Cell.grid[one_d(x, y)]
            if cell in path:
                color = Color.blue
            elif cell in active:
                color = Color.green
            elif cell in visited:
                color = Color.red
            else:
                continue
            pg.draw.rect(screen, color, (pad + (pad + sqr_sz)*x, pad + (pad + sqr_sz)*y, sqr_sz, sqr_sz))


def scr_clear(screen):
    for y in range(sqr_ny):
        for x in range(sqr_nx):
            if Cell.grid[one_d(x, y)].obst:
                color = Color.black
            else:
                color = Color.white

            pg.draw.rect(screen, color, (pad + (pad + sqr_sz)*x, pad + (pad + sqr_sz)*y, sqr_sz, sqr_sz))


def line_tuple(p1, p2, steps = 100):
    line = []
    x, y = p1
    x1, y1 = p2
    dx = (x1 - x)/steps
    dy = (y1 - y)/steps
    for i in range(steps):
        line.append((round(x + dx*i), round(y + dy*i)))
    return line


def setup():
    scr_w = (sqr_sz + pad)*sqr_nx + pad
    scr_h = (sqr_sz + pad)*sqr_ny + pad
    pg.init()

    screen = pg.display.set_mode((scr_w, scr_h))
    screen.fill(Color.gray)
    pg.display.set_caption('A* pathfinding')

    Cell.grid = []
    obstacles = [*line_tuple((30, 15), (15, 15))]

    for y in range(sqr_ny):
        for x in range(sqr_nx):
            obst = False
            if ((x, y) in obstacles or random.randint(0, 3) == 2):
                obst = True
            Cell(x, y, obst)
    scr_clear(screen)
    return screen


def main():
    screen = setup()
    run = False
    FramePerSec = pg.time.Clock()
    FPS = 60

    start = Cell.grid[0]
    active = [start]
    visited = []
    path = []
    i = 0
    while True:
        i = (i+1)%10
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit() 
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                target = Cell.grid[one_d(x//(sqr_sz+pad), y//(sqr_sz+pad))]
                scr_clear(screen)
                pg.display.update()

                start = Cell.grid[0]
                active = [start]
                visited = []
                path = []
                i = 0
                run = True

        if run:
            current = min(active, key = lambda x: (x.tCost(), x.eCost))
            active.remove(current)
            visited.append(current)

            if current == target:
                path = retrace(start, target)
                run = False

            for neighbour in current.get_neighbours():
                if neighbour.obst or neighbour in visited:
                    continue

                nSc = current.sCost + Cell.grid_dist(current, neighbour)
                nEc = Cell.grid_dist(neighbour, target)
                if nSc + nEc < neighbour.tCost() or neighbour not in active:
                    neighbour.sCost = nSc
                    neighbour.eCost = nEc
                    neighbour.parent = current
                    if neighbour not in active:
                        active.append(neighbour)

        if i == 1:
            draw(screen, active, visited, path)
            pg.display.update()
            #FramePerSec.tick(FPS)
                

while __name__ == '__main__':
    main()