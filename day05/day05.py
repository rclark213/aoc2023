import re
import numpy as np

sample = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""



def build_map(starting_line, lines):
    still_building = True
    line_idx = starting_line
    map_rows = []
    while still_building:
        if len(lines[line_idx]) > 0:
            map_rows.append(re.findall(r"\d+", lines[line_idx]))
            line_idx += 1
            if line_idx == len(lines):
                still_building = False
        else:
            still_building = False
    arr = np.array(map_rows, dtype="int")
    arr = arr[arr[:,1].argsort()]
    return arr, line_idx


def map_value(v_in, map):
    if v_in > map[-1,1]:
        row = len(map[:,1])
    else:
        row = next(i for i, val in enumerate(map[:,1]) if val > v_in)
    row = row - 1 if row > 0 else 0
    if v_in <= map[row,1] + map[row,2]:
        v_out = map[row,0] + v_in - map[row,1]
    else:
        v_out = v_in
    return v_out


def loc_from_seed(seed, maps):
    source = seed
    for map in maps:
        dest = map_value(source, map)
        source = dest
    return dest

with open("input05.txt") as f:
    lines = f.read().splitlines()
    seeds = [int(x) for x in re.findall(r"\d+", lines[0])]
    current_line = 3
    maps = []
    # Build all the maps
    for map_idx in range(7):
        maps.append([None])
        maps[map_idx], current_line = build_map(current_line + 2, lines)

    locs = [loc_from_seed(seed, maps) for seed in seeds]
    print(min(locs))


