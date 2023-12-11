import numpy as np

def update_map(map):

    i = 0
    done = False
    while i < map.shape[1]:
        if set(map[:, i]) <= {'.', 'M'}:
            map[:, i] = 'M'
            print(map.shape)
        i += 1
    i = 0
    done = False
    while i < map.shape[1]:
        if set(map[i, :]) <= {'.', 'M'}:
            map[i, :] = 'M'
        i += 1
    return map


def calc_distance(map, factor):
    distance = 0
    galaxies = np.argwhere(map == '#')
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            d1 = abs(galaxies[j][0] - galaxies[i][0]) + abs(galaxies[j][1] - galaxies[i][1])
            top, bottom = sorted([galaxies[i][0], galaxies[j][0]])
            col = map[top:bottom+1, galaxies[i][1]]
            left, right = sorted([galaxies[i][1], galaxies[j][1]])
            row = map[galaxies[i][0], left:right+1]
            m_crosses = np.count_nonzero(col=='M') + np.count_nonzero(row=='M')
            distance += d1 + m_crosses * (factor - 1)
    return distance

with open('input11.txt') as f:
    lines = f.read().splitlines()

lines = [list(line) for line in lines if len(line)>0]

orig_map = np.array(lines)
map = orig_map.copy()
map = update_map(map)

print('Part 1: ', calc_distance(map, 2))
print('Part 2: ', calc_distance(map, 1000000))
