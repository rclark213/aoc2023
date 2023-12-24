import heapq
import numpy as np

file = 'test.txt'
with open(file) as f:
    lines = f.read().splitlines()
yard = []
for line in lines:
    yard.append(list(line))
yard = np.array(yard, dtype='U1')
yard_blank = yard.copy()
yard_blank[yard == '#'] = '.'
start_y, start_x = np.argwhere(yard == 'S')[0]

footprints = {'odd': set(), 'even': {(start_y, start_x)}}
perimeter = [(start_y, start_x)]

for step in range(1, 65):
    step_type = 'odd' if step % 2 == 1 else 'even'
    new_perimeter = []
    for cy, cx in perimeter:
        for ny, nx in [(cy-1, cx), (cy, cx + 1), (cy + 1, cx), (cy, cx - 1)]:
            if 0 <= ny <= yard.shape[0] - 1 and 0 <= nx <= yard.shape[1] - 1:
                if yard[ny, nx] != '#' and (ny, nx) not in footprints[step_type]:
                    footprints[step_type].add((ny, nx))
                    new_perimeter.append((ny, nx))
    perimeter = new_perimeter

print(f"Part 1: {len(footprints[step_type])}")


def translate(y, x, arr):
    # 10x10 grid, (0,0) top left corner... (0, 9) on right edge... (0,10) would map back to (0,0)
    # So y % width of grid --> y_orig? (23,17) -->
    y_orig = y % arr.shape[0]
    x_orig = x % arr.shape[1]
    return y_orig, x_orig

def ambulate(yard, steps, style='finite'):

    start_y, start_x = np.argwhere(yard == 'S')[0]

    footprints = {'odd': set(), 'even': {(start_y, start_x)}}
    perimeter = [(start_y, start_x)]

    for step in range(1,steps + 1):
        step_type = 'odd' if step % 2 == 1 else 'even'
        new_perimeter = []
        for cy, cx in perimeter:
            for ny, nx in [(cy-1, cx), (cy, cx + 1), (cy + 1, cx), (cy, cx - 1)]:
                match style:
                    case 'finite':
                        if 0 <= ny <= yard.shape[0] - 1 and 0 <= nx <= yard.shape[1] - 1:
                            continue
                        nyo, nxo = ny, nx
                    case 'infinite':
                        nyo, nxo = translate(ny, nx, yard)
                if yard[nyo, nxo] != '#' and (ny, nx) not in footprints[step_type]:
                    footprints[step_type].add((ny, nx))
                    new_perimeter.append((ny, nx))
        perimeter = new_perimeter
        if step in [10, 11, 50, 51, 100, 101, 500, 501, 1000, 1001, 5000, 5001]:
            print(f"Steps: {step}   | Tiles: {len(footprints[step_type])}")

ambulate(yard, 500, 'infinite')
ambulate(yard_blank, 500, 'infinite')
print('Part 2: ', len(footprints[step_type]))

# 11x11 Square Results
#   Steps           With Rocks          Without Rocks
#   6               16
#   10              50
#   50              1594
#   100             6536
#   500             167004
#   1000            668697
#   5000            16733044