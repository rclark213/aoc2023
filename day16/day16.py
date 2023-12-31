import numpy as np
from pprint import pprint


def create_grid(file):
    with open(file) as f:
        lines = f.read().splitlines()
    grid = np.array([list(line) for line in lines])
    grid[grid == '\\'] = 'b'
    grid[grid == '/'] = 'f'
    return grid


class Beam:

    def __init__(self, loc, dir):
        self.loc = loc
        self.dir = dir
        self.wake = [loc]
        self.status = 'live'
        self.start()

    def start(self):
        while self.status == 'live':
            self.orient()
            if self.status == 'live':
                self.step()

    def orient(self):

        angle = {'f': {'N': 'E', 'E': 'N', 'S': 'W', 'W': 'S'}, 'b': {'N': 'W', 'E': 'S', 'S': 'E', 'W': 'N'}}
        tile = grid[self.loc]

        if tile in 'fb':
            self.dir = angle[tile][self.dir]
        elif tile == '-':
            if self.dir in 'NS':
                self.split()
                self.status = 'dead'
        elif tile == '|':
            if self.dir in 'EW':
                self.split()
                self.status = 'dead'
        self.wall_check()

    def wall_check(self):
        if (self.dir == 'N' and self.loc[0] == 0) or \
                (self.dir == 'E' and self.loc[1] == grid.shape[1] - 1) or \
                (self.dir == 'S' and self.loc[0] == grid.shape[0] - 1) or \
                (self.dir == 'W' and self.loc[1] == 0):
            self.status = 'dead'

    def split(self):
        self.status = 'dead'
        if self.loc not in splits:
            splits.append(self.loc)
            if self.dir in 'NS':
                new_dir = 'EW'
            elif self.dir in 'EW':
                new_dir = 'NS'
            beams.append(Beam(self.loc, new_dir[0]))
            beams.append(Beam(self.loc, new_dir[1]))

    def step(self):
        tile = grid[self.loc]
        if self.dir == 'N':
            self.loc = (self.loc[0] - 1, self.loc[1])
        elif self.dir == 'E':
            self.loc = (self.loc[0], self.loc[1] + 1)
        elif self.dir == 'S':
            self.loc = (self.loc[0] + 1, self.loc[1])
        elif self.dir == 'W':
            self.loc = (self.loc[0], self.loc[1] - 1)
        self.wake.append(self.loc)


example = 'test.txt'
real = 'input.txt'
grid = create_grid(real)


def energize(start_loc, start_dir):
    global splits, beams
    splits = []
    beams = []
    beams.append(Beam(start_loc, start_dir))

    energized = np.full_like(grid, fill_value='0', dtype='int')
    for beam in beams:
        for point in beam.wake:
            energized[point] = '1'
    return np.sum(energized)


t = 0
for i in range(grid.shape[0]):
    e1 = energize((i, 0), 'E')
    e2 = energize((i, grid.shape[1]-1), 'W')
    t = max(e1, e2, t)

for i in range(grid.shape[1]):
    e1 = energize((0, i), 'S')
    e2 = energize((grid.shape[0]-1, i), 'N')
    t = max(e1, e2, t)

print('t: ', t)
