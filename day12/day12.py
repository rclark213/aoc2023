import re
from collections import namedtuple
from itertools import permutations, product
import numpy as np
import math

Row = namedtuple('Row', ['layout', 'dist'])

def expand_rows(rows):
    rows_expanded = []
    for layout, dist in rows:
        layout_new = '?'.join([layout] * 5)
        dist_new = dist * 5
        rows_expanded.append(Row(layout_new, dist_new))
    return rows_expanded

# def assign_musts(layout, dist):
#     for i in range(len(layout)):
#         if layout[i] == '?':
#             test_layout = layout[:i] + '#' + layout[i+1:]


def brute_force(rows):
    possible = 0
    i = 0
    for layout, dist in rows:
        print(i)
        prog = build_regex(dist)
        q_locs = [pos for pos, char in enumerate(layout) if char == '?']
        for perm in product('.#', repeat=len(q_locs)):
            ll = list(layout)
            for i, loc in enumerate(q_locs):
                ll[loc] = perm[i]
            if prog.fullmatch(''.join(ll)):
                possible += 1
    i = i+1
    return possible


def generate_patterns(spaces,hashes):
    perms = permutations(range(spaces), r=hashes)
    pos_sets = []
    patterns = []
    for perm in perms:
        if set(perm) not in pos_sets:
            pos_sets.append(set(perm))
            a = ['.'] * spaces
            for loc in perm:
                a[loc] = '#'
            patterns.append(''.join(a))
    return patterns

def get_combos(spots, total, current=None, combos=None):
    if current is None:
        current = []
    if combos is None:
        combos = []
    if len(current) != spots - 1:
        c = current.copy()
        c.append(0)
        rem = sum(current)
        for x in range(total + 1 - rem):
            c[-1] = x
            get_combos(spots, total, c, combos)
    else:
        t = current.copy()
        t.append(total - sum(t))
        combos.append(t)
        print('Combo length: ', len(combos))
    return combos

# Define a regex pattern that determines if a pattern is valid for the distribution

def build_regex(dist):
    regex = r"\.*"
    for i, n in enumerate(dist):
        regex = regex + r'#{' + str(n) + r'}\.' + (r'+' if i != len(dist) - 1 else '*')
    return re.compile(regex)

# Update all the ? locations with every combination of . and #, and compare against the regex

def iterate_blanks(rows):
    possible = 0
    i = 0
    for layout, dist in rows:
        print(i)
        prog = build_regex(dist)
        q_locs = [pos for pos, char in enumerate(layout) if char == '?']
        q_count = len(q_locs)
        hash_count = layout.count('#')
        hash_all = sum(dist)
        hash_left = hash_all - hash_count
        dot_left = q_count - hash_left
        j = 0
        patterns = generate_patterns(q_count, hash_left)
        # print(choices)
        print('meth 2: ', len(patterns))
        for pattern in patterns:
            # print('Perm:', j)
            ll = list(layout)
            for k, loc in enumerate(q_locs):
                ll[loc] = pattern[k]
            if prog.fullmatch(''.join(ll)):
                possible += 1
            j += 1
        i = i+1
    return possible

#  For the given distribution, generates every possible pattern that can possibly meet the criteria,
#  treating the groups as "cars" and the unnecessary periods as "gaps". Gaps can have any number of periods
#  and still fit the distribution profile, so long as the total characters equals the row length.
#  {gap} {car} {gap} {car} {gap} {car} {gap}
#  For a (1, 2, 3) distribution and length of 9, that leaves 1 to assign after the necessary periods between cars.
#  {gap0} #. {gap1} ##. {gap2} ### {gap3} possibilities include
#  .#.##.###  |  #..##.###  |  #.##..###  |  #.##.###.

def valid_patterns(layout, dist):
    cars = []
    for i, run in enumerate(dist):
        if i < len(dist) - 1:
            cars.append('#' * run + '.')
        else:
            cars.append('#' * run)
    print('Cars: ', cars)
    car_sum = sum([len(car) for car in cars])
    leftover_space = len(layout) - car_sum
    gap_combos = get_combos(len(cars) + 1, leftover_space)
    print('# Combos: ', len(gap_combos))
    # print('Combos: ', gap_combos)
    patterns = []
    for combo in gap_combos:
        pattern = ''
        for i, val in enumerate(combo):
            if i < len(cars):
                pattern += '.' * val + cars[i]
            else:
                pattern += '.' * val
        patterns.append(pattern)
    return patterns

def walk_through(layout, dist):
    dist_idx = 0
    if dist_idx < len(dist - 1):
        run = '#' * dist[dist_idx] + '.'
    for a, char in enumerate(layout):
        if char == '?':
            test_layout = layout[:a] + '#' + layout[a+1:]


def main():

    # Get Part 1 rows
    rows = []
    with open('input12.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            result = re.split(r"[\s,]", line)
            rows.append(Row(result[0], [int(x) for x in result[1:]]))

    print('Part 1 (brute force): ', brute_force(rows))

    for row in rows:
        patterns = valid_patterns(row.layout, row.dist)

    # Expand Rows
    rows_expanded = expand_rows(rows)


    for i, row in enumerate(rows_expanded[1:2]):
        print(i)
        patterns = valid_patterns(row.layout, row.dist)
        i += 1



main()




# possible = method2(rows)
#
# print('Part 1: ', possible)
#
# # Part 2:
#

#
# possible = method2(fullrows)
#
# print('Part 2: ', possible)


