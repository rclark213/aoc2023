import numpy as np
from collections import namedtuple
from pprint import pprint
import copy

class Node:

    def __init__(self, point):
        self.y, self.x = point
        self.paths_in = []
        self.paths_out = []

    def find_exits(self):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighbors = []
        exits = []
        paths_out = []
        valid = ['^', '>', 'v', '<']
        for d, v in zip(directions, valid):
            dy, dx = d
            print(self.y, self.x)
            if grid[self.y + dy][self.x + dx] == v:
                exits.append((self.y + dy, self.x + dx))
        for e in exits:
            paths_out.append(walk_path([(self.y, self.x), e], grid))
        return paths_out

def parse_input(file):
    with open(file) as f:
        lines = f.read().splitlines()
        grid = [list(line) for line in lines]
    return grid

def walk_path(path, grid):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    walking = True
    while walking:
        py, px = path[-1]
        print('Walking: ', py, px)
        neighbors = []
        for dy, dx in directions:
            npy, npx = py + dy, px + dx
            if 0 <= npy < len(grid) and 0 <= npx < len(grid[0]):
                if grid[npy][npx] in '.<>^v' and (npy, npx) not in path:
                    neighbors.append((npy, npx))
        match len(neighbors):
            case 1:
                print('1 neighbor')
                path.extend(neighbors)
                print('Neighbor: ', neighbors[0][0])
                print('Grid length', len(grid))
                if neighbors[0][0] == len(grid) - 1:
                    print('Hit maze exit')
                    walking = False
            case _:
                print(f"{len(neighbors)} neighbors")
                walking = False
    return path


def build_graph(grid):
    paths = dict()
    nodes = dict()
    start = (0, grid[0].index('.'))
    end = (len(grid)-1, grid[-1].index('.'))
    first_path = walk_path([start], grid)
    nodes.update({0: Node(start)})
    nodes.update({1: Node(end)})
    paths.update({0: first_path})
    nodes.update({2: Node(first_path[-1])})
    nodes[0].paths_out.append(0)
    nodes[2].paths_in.append(0)
    queue = [2]
    building = True
    while building:
        current_node = nodes[queue[0]]
        new_paths = current_node.find_exits()
        for p in new_paths:
            new_path_key = len(paths)
            paths.update({new_path_key: p})  # Add the path(list of coordinates) to the path dict
            current_node.paths_out.append(new_path_key)  # Add the path key to the current node's list of paths out
            if p[-1] not in [(node.y, node.x) for node in nodes.values()]:
                new_node_key = len(nodes)
                nodes.update({new_node_key: Node(p[-1])}) # Add a node
                nodes[new_node_key].paths_in.append(new_path_key)
                if p[-1][1] != len(grid) - 1:
                    queue.append(new_node_key)
            else:
                for k,v in nodes.items():
                    if p[-1] == (v.y, v.x):
                        nodes[k].paths_in.append(new_path_key)
        queue.pop(0)
        print('Queue: ', queue)
        for node in queue:
            print(nodes[node].y, nodes[node].x)
        if len(queue) == 0:
            building = False
    return nodes, paths

def get_all_nodes(grid):
    nodes = dict()
    pass


grid = parse_input('input.txt')

nodes, paths = build_graph(grid)
print('')

def node_from_yx(coordinate):
    for k, node in nodes.items():
        if (node.y, node.x) == coordinate:
            return k
    return None

def chain_length(chain):
    steps = 0
    for p in chain:
        steps += len(paths[p]) - 1
    steps += 1
    return steps


def traverse_paths(node):
    chains = []
    for p in nodes[node].paths_out:
        if p in nodes[1].paths_in:
            chains.append([p])
        else:
            new_chain = [p]
            lastcoord = paths[p][-1]
            nextnode = node_from_yx(lastcoord)
            nextchain = traverse_paths(nextnode)
            new_chain.extend(nextchain)
            chains.append(new_chain)
    lengths = [chain_length(chain) for chain in chains]
    return chains[lengths.index(max(lengths))]

max_length = chain_length(traverse_paths(0)) - 1 # For the first step
print('Part 1: ', max_length)



# nodeletters = 'ABCDEFGHIJKLMNOP'
# pathletters = 'abcdefghijklmnop'
#
# checkgrid = copy.deepcopy(grid)
#
# for line in grid:
#     print(''.join(line))
#
# print('')
#
# for k,v in paths.items():
#     for py, px in v:
#         checkgrid[py][px] = pathletters[k]
#
# for k,v in nodes.items():
#     checkgrid[v.y][v.x] = nodeletters[k]
#
# for line in checkgrid:
#     print(''.join(line))




