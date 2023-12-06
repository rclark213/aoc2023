import re
import numpy as np

def get_lines(file):
    with open(file) as f:
        lines = f.read().splitlines()
    return lines


def build_maps(lines):
    (seed2soil, soil2fert, fert2water, water2light, light2temp, temp2hum, hum2loc) = ([], [], [], [], [], [], [])
    for line in lines:
        items = line.split(' ')
        if items[0] == 'seeds:':
            seeds = [int(x) for x in re.findall(r"\d+", line)]
            seed_ranges = [range(x, x + seeds[i + 1]) for i, x in enumerate(seeds) if i % 2 == 0]
        elif len(items) == 2:
            if line[0] == 'seed-to-soil': currMap = seed2soil
            if line[0] == 'soil-to-fertilizer': currMap = soil2fert
            if line[0] == 'fertilizer-to-water': currMap = fert2water
            if line[0] == 'water-to-light': currMap = water2light
            if line[0] == 'light-to-temperature': currMap = light2temp
            if line[0] == 'temperature-to-humidity': currMap = temp2hum
            if line[0] == 'humidity-to-location': currMap = hum2loc
        elif len(items) == 3:
            a, b, c = items
            currMap.append((range(b, b+c), a-b))
        else:
            pass
    return seed2soil, soil2fert, fert2water, water2light, light2temp, temp2hum, hum2loc








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

def ranges_from_map(map):
    source_ranges = []
    sink_ranges = []
    curval = 0
    for start_sink, start_source, length in zip(map[:,0], map[:, 1], map[:, 2]):
        if start_source > curval:
            source_ranges.append(range(curval, start_source))
            sink_ranges.append(range(curval, start_source))
        source_ranges.append(range(start_source, start_source + length))
        sink_ranges.append(range(start_sink, start_sink + length))
        curval = start_source + length
    return source_ranges, sink_ranges

def find_row(v_in, map):
    if v_in > map[-1,1]:
        row = len(map[:,1])
    else:
        row = next(i for i, val in enumerate(map[:,1]) if val > v_in)
    row = row - 1 if row > 0 else 0
    return row

def map_value(v_in, map):
    row = find_row(v_in, map)
    if v_in <= map[row,1] + map[row,2]:
        v_out = map[row,0] + v_in - map[row,1]
    else:
        v_out = v_in
    return v_out


def source_to_sink(source_val, range_map):
    idx = next(row for row, rng in enumerate(range_map['source']) if source_val in rng)
    sink_val = range_map['sink'][idx].start + (source_val - range_map['source'][idx].start)
    return sink_val


def loc_from_seed(seed, maps):
    source = seed
    for map in maps:
        dest = map_value(source, map)
        source = dest
    return dest


def build_subranges(input_range, range_map):
    subranges_source = []
    subranges_sink = []
    start_idx = next(i for i, rng in enumerate(range_map['source']) if input_range.start in rng)
    stop_idx = next(i for i, rng in enumerate(range_map['source']) if input_range.stop - 1 in rng)
    for current_range_source, current_range_sink in zip(
            range_map['source'][start_idx: stop_idx + 1], range_map['sink'][start_idx: stop_idx + 1]):
        if input_range.start in current_range_source:
            source_start = input_range.start
            sink_start = current_range_sink.start + (input_range.start - current_range_source.start)
        else

            subranges_source.append(range(input))
        subranges_source.append(range(
            input_range.start if input_range.start in current_range_source else current_range_source.start,
            input_range.stop if input_range.stop - 1 in current_range_source else current_range_source.stop))
    for subrange in subranges_source:
        subranges_sink.append(range(source_to_sink(subrange.start, range_map), source_to_sink(subrange.stop, range_map)))
    return subranges_source, subranges_sink



with open("input05.txt") as f:
    lines = f.read().splitlines()
    # lines = sample.splitlines()  # Toggle comment to test
    seeds = [int(x) for x in re.findall(r"\d+", lines[0])]
    current_line = 1
    maps = []
    # Build all the maps
    for map_idx in range(7):
        maps.append([None])
        maps[map_idx], current_line = build_map(current_line + 2, lines)
    # Build a range map for each map
    # Each range map consists of a source and sink array of ranges with full coverage from zero to the highest number in the source map

    range_maps = []
    for map in maps:
        source_ranges, sink_ranges = ranges_from_map(map)
        range_maps.append(dict([("source", source_ranges), ("sink", sink_ranges)]))

    locs = [loc_from_seed(seed, maps) for seed in seeds]
    print("Part 1 answer: ", min(locs))

# Part 2:

seed_ranges = [range(x, x+seeds[i+1]) for i, x in enumerate(seeds) if i % 2 == 0]

print("Sink: ", source_to_sink(60, range_maps[0]))

x, y = build_subranges(seed_ranges[0], range_maps[0])
print(x)
print(y)
a = []
b = []
for elem in x:
    a.append(elem.stop - elem.start)
for elem in y:
    b.append(elem.stop - elem.start)
print(a)
print(b)
print('hi')

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
56 93 4

"""