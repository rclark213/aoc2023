import numpy as np
from collections import namedtuple
import math
import time

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.cost = grid[position]

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def above(loc):
    return (loc[0] - 1, loc[1])

def rightof(loc):
    return (loc[0], loc[1] + 1)

def below(loc):
    return (loc[0] + 1, loc[1])

def leftof(loc):
    return (loc[0], loc[1] - 1)

def get_neighbors(node):
    up = Node(None, above(node.position))
    right = Node(None, rightof(node.position))
    down = Node(None, below(node.position))
    left = Node(None, leftof(node.position))
    return up, right, down, left

def h_val(node):
    return abs(target.position[0] - node.position[0]) + abs(target.position[1] - node.position[1])


open_list = []
closed_list = []

example = 'test.txt'
real = 'input.txt'

with open(example) as f:
    lines = f.read().splitlines()

grid = []

for line in lines:
    grid.append([int(char) for char in line])

grid = np.array(grid)
grid = np.pad(grid, 1, mode='constant', constant_values=1000)


start = Node(None, (1,1))
start.g = start.h = start.f = 0
target = Node(None, (grid.shape[0] - 2, grid.shape[1] - 2))
target.g = target.h = target.f = 0

open_list.append(start)

def a_star():
    while open_list:

        open_list.sort(key=lambda node: node.f)
        print('Open list: ')
        print([node.position for node in closed_list])
        current_node = open_list.pop(0) # Remove smallest f-value from open list and put it in closed list
        print('Current Node: ', current_node.position)
        closed_list.append(current_node)
        print('Closed list: ')
        print([node.position for node in closed_list])
        open_locs = [node.position for node in open_list]
        closed_locs = [node.position for node in closed_list]
        if current_node.position == target.position:
            print('Yer a pathfinding Wizard Harry!')
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
            break
        for neighbor in get_neighbors(current_node):
            if neighbor.position in closed_locs:
                continue
            neighbor.g = current_node.g + neighbor.cost
            neighbor.h = h_val(neighbor)
            neighbor.f = neighbor.g + neighbor.h
            if neighbor.position in open_locs and neighbor.g > open_list[open_locs.index(neighbor.position)].g:
                continue
            neighbor.parent = current_node
            open_list.append(neighbor)

a_star()

    # time.sleep(0.2)



