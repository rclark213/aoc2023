import re
import numpy as np
from collections import Counter
from pprint import pprint

with open('input.txt') as f:
    lines = f.read().splitlines()

rockmap = []
for line in lines:
    rockmap.append(list(line))

rockmap = np.array(rockmap)
original_map = rockmap.copy()


def roll_rocks(rockmap):
    rolled_map = []
    for i in range(rockmap.shape[0]):
        groups = re.split(r"#", ''.join(rockmap[:,i]))
        rolled = []
        for group in groups:
            rolled.append(''.join([x for x in group if x == 'O']) + ''.join([x for x in group if x == '.']))
        rolled_map.append(list('#'.join(rolled)))

    rolled_map = np.transpose(np.array(rolled_map))
    return rolled_map

rolled_map = roll_rocks(rockmap)

def score_board(rolled_map):
    rows, cols = np.where(rolled_map == 'O')
    score = sum(rolled_map.shape[0] - rows)
    return score
print('')

def get_hash(rockmap):
    return hash(tuple(map(tuple, rockmap == 'O')))

def spin_cycle(rockmap):
    for i in range(4):
        rockmap = roll_rocks(rockmap)
        rockmap = np.rot90(rockmap, k=-1)
    return rockmap

score = score_board(rolled_map)

print('Part 1: ', score)

# Part 2


# for i in range(1000):
#     rockmap = roll_rocks(np.rot90(rockmap, k=-1))
#     score = score_board(rockmap)
#     scores.append(score)
#
#
# A = Counter(scores)
#
# print(A.most_common())

cycle = 0
repeated = False
hashes = [get_hash(rockmap)]

while not repeated:
    rockmap = spin_cycle(rockmap)

    pprint(rockmap)
    map_hash = get_hash(rockmap)
    cycle += 1
    print(cycle)
    print(score_board(rockmap))
    if map_hash in hashes:
        repeated = True
        hash_index = hashes.index(map_hash)
        cycle_length = cycle - hash_index
        subindex = (1000000000 - cycle) % cycle_length
        a = rockmap.copy()
        b = np.rot90(rockmap, k=-1)
        print(a)
        print('')
        print(b)

        for i in range(subindex):
            rockmap = spin_cycle(rockmap)
        score = score_board(rockmap)

        print('Hash_index: ', hash_index)
        print('Current cycle: ', cycle)

    else:
        hashes.append(get_hash(rockmap))

print('Part 2: ', score)
# for i in range(1100):
#     rolled_map = roll_rocks(np.rot90(rolled_map, k=-1))
#
# billion_score = score_board(rolled_map)
#
# print('Part 2: ', billion_score)

