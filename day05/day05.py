import re
import numpy as np

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

def loc_from_seed(seed):
    soil = map_value(seed, seed_to_soil_map)
    fertilizer = map_value(soil, soil_to_fertilizer_map)
    water = map_value(fertilizer, fertilizer_to_water_map)
    light = map_value(water, water_to_light_map)
    temp = map_value(light, light_to_temp_map)
    humidity = map_value(temp, temp_to_humidity_map)
    loc = map_value(humidity, humidity_to_loc_map)
    return loc

with open("input05.txt") as f:
    lines = f.read().splitlines()
    seeds = [int(x) for x in re.findall(r"\d+", lines[0])]
    current_line = 3
    seed_to_soil_map, current_line = build_map(current_line, lines)
    soil_to_fertilizer_map, current_line = build_map(current_line + 2, lines)
    fertilizer_to_water_map, current_line = build_map(current_line + 2, lines)
    water_to_light_map, current_line = build_map(current_line + 2, lines)
    light_to_temp_map, current_line = build_map(current_line + 2, lines)
    temp_to_humidity_map, current_line = build_map(current_line + 2, lines)
    humidity_to_loc_map, current_line = build_map(current_line + 2, lines)

locs = [loc_from_seed(seed) for seed in seeds]
print(min(locs))


