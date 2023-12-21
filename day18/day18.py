import re
import numpy as np
from matplotlib.path import Path
from scipy.ndimage import label

class Perimeter:

    def __init__(self, head):
        self.head = head
        self.vals = [head]
        self.tail = head
        self.vertices = [self.tail]

    def expand(self, dir, steps):
        if dir == 'U':
            self.vals.extend([(self.tail[0] - i, self.tail[1]) for i in range(1, steps + 1)])
        elif dir == 'D':
            self.vals.extend([(self.tail[0] + i, self.tail[1]) for i in range(1, steps + 1)])
        elif dir == 'R':
            self.vals.extend([(self.tail[0], self.tail[1] + i) for i in range(1, steps + 1)])
        elif dir == 'L':
            self.vals.extend([(self.tail[0], self.tail[1] - i) for i in range(1, steps + 1)])
        self.tail = self.vals[-1]
        self.vertices.append(self.tail)

    def shift(self, shift_y, shift_x):
        self.head = (self.head[0] + shift_y, self.head[1] + shift_x)
        self.tail = (self.tail[0] + shift_y, self.tail[1] + shift_x)
        self.vals = [(val[0] + shift_y, val[1] + shift_x) for val in self.vals]
        self.vertices = [(vertex[0] + shift_y, vertex[1] + shift_x) for vertex in self.vertices]


with open('input.txt') as f:
    lines = f.read().splitlines()

instructions = []
for line in lines:
    instructions.append(re.match(r'([URDL]) (\d+) .+#([a-z0-9]{6})', line).groups())

perimeter = Perimeter((0,0))
for line in instructions:
    perimeter.expand(line[0], int(line[1]))

topbound = min([val[0] for val in perimeter.vals])
bottombound = max([val[0] for val in perimeter.vals])
leftbound = min([val[1] for val in perimeter.vals])
rightbound = max([val[1] for val in perimeter.vals])

height = bottombound - topbound + 1
width = rightbound - leftbound + 1

perimeter.shift(-topbound, -leftbound)

grid = np.full((height, width), '.', dtype='U1')
idx_list = np.array(perimeter.vals)
grid[idx_list[:,0], idx_list[:,1]] = '#'
grid2 = grid.copy()

count = 0
for i, row in enumerate(grid):
    loc = 'outside'
    for j, col in enumerate(row):
        if loc == 'outside':
            if col == '#':
                count += 1
                loc = 'inward'
                continue
            elif col == '.':
                continue
        elif loc == 'inward':
            if col == '#':
                count += 1
                continue
            elif col == '.':
                grid[i,j] = 'O'
                loc = 'inside'
                count += 1
                continue
        elif loc == 'inside':
            if col == '.':
                grid[i,j] = 'O'
                count += 1
                continue
            elif col == '#':
                count += 1
                loc = 'outward'
                continue
        elif loc == 'outward':
            if col == '#':
                count += 1
                continue
            elif col == '.':
                loc = 'outside'
                continue



print(f'Count: {count}')

x, y = np.meshgrid(np.arange(width), np.arange(height))
x, y = x.flatten(), y.flatten()
points = np.vstack((x,y)).T
p = Path(perimeter.vertices[:-1])
xygrid = p.contains_points(points)
mask = xygrid.reshape(width,height)

print(np.sum(mask) + len(perimeter.vals) - 1)

# 93240 too high
# 89330 too low
# 84642 too low

non_path_arr = np.ones_like(grid, dtype=bool)
r = [val[0] for val in perimeter.vals]
c = [val[1] for val in perimeter.vals]
non_path_arr[r,c] = False
label, num_features = label(non_path_arr)

print('done')

print(f'Sci total: {np.sum(label==0) + np.sum(label==4)}')
