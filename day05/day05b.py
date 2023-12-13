import re


def get_lines(file): # Gets the raw lines from the file as a list
    with open(file) as f:
        lines = f.read().splitlines()
    return lines

def build_data(lines): # Builds the seeds, seed_ranges, and maps.
    maps = {
        'seed2soil': [],
        'soil2fert': [],
        'fert2water': [],
        'water2light': [],
        'light2temp': [],
        'temp2hum': [],
        'hum2loc': []
    }
    for line in lines:
        items = line.split(' ')
        if items[0] == 'seeds:':
            seeds = [int(x) for x in re.findall(r"\d+", line)]
            seed_ranges = [range(x, x + seeds[i + 1]) for i, x in enumerate(seeds) if i % 2 == 0]
        elif len(items) == 2:
            if items[0] == 'seed-to-soil': currMap = 'seed2soil'
            if items[0] == 'soil-to-fertilizer': currMap = 'soil2fert'
            if items[0] == 'fertilizer-to-water': currMap = 'fert2water'
            if items[0] == 'water-to-light': currMap = 'water2light'
            if items[0] == 'light-to-temperature': currMap = 'light2temp'
            if items[0] == 'temperature-to-humidity': currMap = 'temp2hum'
            if items[0] == 'humidity-to-location': currMap = 'hum2loc'
        elif len(items) == 3:
            a, b, c = (int(items[0]), int(items[1]), int(items[2]))
            maps[currMap].append((range(b, b + c), a - b))
        else:
            pass
    for k,v in maps.items():
        v.sort(key=lambda x: x[0].start) # Sort ascending
        # Insert map ranges for any gaps
        v_new = v.copy()
        offset = 0
        for i in range(len(v)-1):
            if v[i][0].stop != v[i+1][0].start:
                v_new.insert(i+1+offset, (range(v[i][0].stop, v[i+1][0].start), 0))
                offset += 1
        v = v_new.copy()
        maps.update({k:v})
    return seeds, seed_ranges, maps


def translate_range(rng, map): # Turn a single source range into one or more destination ranges
    # Assumption: mapped ranges are contiguous (well that was a bad assumption)
    new_ranges = []
    overlap = True
    working_range = rng
    map_span = range(map[0][0].start, map[-1][0].stop)
    # Take care of portions of range outside of mapped range
    if working_range.start not in map_span and (working_range.stop - 1) in map_span:
        new_ranges.append(range(working_range.start, map_span.start))
        working_range = range(map_span.start, working_range.stop)
    if working_range.start in map_span and (working_range.stop - 1) not in map_span:
        new_ranges.append(range(map_span.stop, working_range.stop))
        working_range = range(working_range.start, map_span.stop)
    if working_range.start not in map_span and (working_range.stop - 1) not in map_span:
        new_ranges.append(working_range)
        overlap = False

    if overlap:
        for i, entry in enumerate(map):
            line_range = entry[0]
            offset = entry[1]
            if working_range.start in line_range:
                # Each of these situations assumes the beginning of our working range is inside the map entry
                # Situation 1: the working range extends beyond the current map entry (line range)
                if (working_range.stop - 1) not in line_range:
                    new_ranges.append(range(working_range.start + offset, line_range.stop + offset))
                    working_range = range(line_range.stop, working_range.stop)
                # Situation 2: the working range is completely within the current map entry
                else:
                    new_ranges.append(range(working_range.start + offset, working_range.stop + offset))
    new_ranges.sort(key=lambda r: r.start)
    return new_ranges

def translate_multiple_ranges(rng_list, map): # Convert multiple source ranges to destination ranges
    all_new_ranges = []
    for rng in rng_list:
        all_new_ranges.extend(translate_range(rng, map))
    return all_new_ranges

def cascade_ranges(seed_ranges, maps): # Cascade seed ranges all the way to location ranges
    working_ranges = seed_ranges
    for map in maps.values():
        working_ranges = translate_multiple_ranges(working_ranges, map)
    return working_ranges

lines = get_lines("input05.txt")
seeds, seed_ranges, maps = build_data(lines)
seeds_as_ranges = [range(seed, seed + 1) for seed in seeds]

# Part 1
cascaded_ranges = cascade_ranges(seeds_as_ranges, maps) # Basically retrofitting Part 2 solution to Part 1
print('Part 1: ', min([rng.start for rng in cascaded_ranges]))

# Part 2
cascaded_ranges = cascade_ranges(seed_ranges, maps)
print("Part 2: ", min([rng.start for rng in cascaded_ranges]))