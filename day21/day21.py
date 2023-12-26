import heapq
import numpy as np
import csv
from scipy.optimize import curve_fit

file = 'input.txt'
with open(file) as f:
    lines = f.read().splitlines()
yard = []
for line in lines:
    yard.append(list(line))
yard = np.array(yard, dtype='U1')
yard_blank = yard.copy()
yard_blank[yard == '#'] = '.'

# Translates a coordinate from one of the replicated yards to the origin yard coordinate

def translate(y, x, arr):
    y_orig = y % arr.shape[0]
    x_orig = x % arr.shape[1]
    return y_orig, x_orig

def build_valid_dirs_dict(yard):
    valid_dirs_dict = dict()
    for r in range(yard.shape[0]):
        for c in range(yard.shape[1]):
            if yard[r,c] != '#':
                valid_dirs = []
                dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                for dy, dx in dirs:
                    py, px = r+dy, c+dx
                    py = 0 if py == yard.shape[0] else py
                    px = 0 if px == yard.shape[1] else px
                    if yard[py, px] != '#':
                        valid_dirs.append((dy, dx))
                valid_dirs_dict.update({(r, c): valid_dirs})
    return valid_dirs_dict


def ambulate(yard, steps, style='finite'):
    with open('output.txt', 'w') as f:
        wr = csv.writer(f)
        tile_count_full = []
        tile_count_odd = []
        tile_count_even = []
        out = []
        vdd = build_valid_dirs_dict(yard)
        start_y, start_x = np.argwhere(yard == 'S')[0]
        footprints = {'odd': set(), 'even': {(start_y, start_x)}}
        perimeter = [(start_y, start_x)]

        for step in range(1,steps + 1):
            step_type = 'odd' if step % 2 == 1 else 'even'
            new_perimeter = []
            for cy, cx in perimeter:
                for ny, nx in [(cy+dy, cx+dx) for dy, dx in vdd[translate(cy, cx, yard)]]:
                    match style:
                        case 'finite':
                            if 0 <= ny <= yard.shape[0] - 1 and 0 <= nx <= yard.shape[1] - 1:
                                continue
                            nyo, nxo = ny, nx
                        case 'infinite':
                            nyo, nxo = translate(ny, nx, yard)
                    if (ny, nx) not in footprints[step_type]:
                        footprints[step_type].add((ny, nx))
                        new_perimeter.append((ny, nx))
            perimeter = new_perimeter
            tile_count_full.append(len(footprints['even']) + len(footprints['odd']))
            if step_type == 'odd':
                tile_count_odd.append(len(footprints[step_type]))
                wr.writerow([step, len(footprints[step_type])])
            else:
                tile_count_even.append(len(footprints[step_type]))

            if step in [10, 11, 12, 13, 50, 51, 52, 53, 100, 101, 102, 103, 500, 501, 502, 503, 1000, 1001, 1002, 1003]:
                out.append((step, len(footprints[step_type])))
                print(f"Steps: {step}   | Tiles: {len(footprints[step_type])}")

    return (tile_count_odd, tile_count_even, tile_count_full)

vdd = build_valid_dirs_dict(yard)

(tile_count_odd, tile_count_even, tile_count_full) = ambulate(yard, 1000, 'infinite')
# out2 = ambulate(yard_blank, 500, 'infinite')

# table = [(a[0], a[1], b[1], a[1]/b[1]) for a, b in zip(out1, out2)]
# for line in table:
#     print(line)

xdata = np.array([64, 64+131, 64+131*2])
ydata = np.array(tile_count_full)[(64, 64+131, 64+131*2),]
print(xdata)
print(ydata)
[a, b, c] = np.polyfit(xdata, ydata, 2)
print(f"a: {a}, b: {b}, c: {c}")
target_steps = 26501365
part2 = a * target_steps ** 2 + b * target_steps + c
print(f"Part 2: {part2}")
# 479701115008039 too low
# 566477486812956 try 2 (too low)
# 400934135462696 (too low)
# 702322346863225 (too high)
# 608300546852599 (polyfit 1 -
# 1216305722146183 (polyfit 2 --- too high)

# am I dumb? try the input squared.



