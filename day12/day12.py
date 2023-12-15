import functools
import re
from collections import namedtuple
from itertools import permutations, product
import numpy as np
import math
from functools import cache
import time

Row = namedtuple('Row', ['layout', 'dist'])

def expand_rows(rows):
rows_expanded = []
for layout, dist in rows:
    layout_new = '?'.join([layout] * 5)
    dist_new = dist * 5
    rows_expanded.append(Row(layout_new, dist_new))
return rows_expanded




def brute_force(rows):

    @functools.cache
    def get_product(r):
        perms = product('.#', repeat=r)
        return perms

    possible = 0
    i = 0
    for layout, dist in rows:
        print(i)
        prog = build_regex(dist)
        q_locs = [pos for pos, char in enumerate(layout) if char == '?']
        perms = get_product(len(q_locs))
        for perm in perms:
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
        c = []
    else:
        c = list(current).copy()
    if combos is None:
        cm = []
    else:
        cm = list(combos).copy()
    if len(c) != spots - 1:
        c.append(0)
        rem = sum(c)
        for x in range(total + 1 - rem):
            c[-1] = x
            get_combos(spots, total, tuple(c), tuple(cm))
    else:
        c.append(total - sum(c))
        cm.append(c)
        print('Combo length: ', len(cm))
    return tuple(cm)

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

    def topoff(working, idx):
        if len(working) < len(original):
            working = working + original[idx:]
        return working

    def walkback(forks, p_idx, working):
        (s_idx, p_idx) = forks.pop()
        working = working[:s_idx] + '.' + original[s_idx + 1:]
        s_idx += 1
        return s_idx, p_idx, working

    def show(working, forks, s_idx, pattern):
        print('-----------------')
        print('Pattern: ', pattern)
        print('')
        bottom = [' '] * (len(working) + 1)
        top = bottom.copy()
        for fork in forks:
            top[fork[0]] = str(fork[1])
        bottom[s_idx] = '^'
        bottom = ''.join(bottom)
        top = ''.join(top)
        print(top)
        print(working + '   ')
        print(bottom)
        print('------------------')
        time.sleep(0.1)

    original = layout
    working = layout
    searching = True
    s_idx = 0
    p_idx = 0
    forks = []
    patterns = dist_to_patterns(dist)
    options = []

    while searching:
        pattern = patterns[p_idx]
        # show(working, forks, s_idx, pattern)
        # print()
        # If the remaining space can't fit the current pattern...
        remaining = len(working) - (s_idx)
        if remaining < len(pattern):
            # print('Issue 1')
            if len(forks) == 0:
                break
            else:
                s_idx, p_idx, working = walkback(forks, p_idx, working)
                continue
        # If a period...
        if working[s_idx] == '.':
            s_idx += 1
            continue
        elif working[s_idx] == '#':
            view = working[s_idx: s_idx + len(pattern)]
            if check_compatibility(view, pattern):
                working = working[:s_idx] + pattern
                p_idx += 1
                s_idx += len(pattern)
                working = topoff(working, s_idx)
            else:
                # print('Issue 2')
                if len(forks) == 0:
                    break
                else:
                    s_idx, p_idx, working = walkback(forks, p_idx, working)
                    continue
        elif working[s_idx] == '?':
            view = working[s_idx: s_idx + len(pattern)]
            assessment = assess(view, pattern)
            # print(assessment)
            if assessment == 'broken':
                if len(forks) == 0:
                    break
                else:
                    s_idx, p_idx, working = walkback(forks, p_idx, working)
                    continue
            elif assessment == 'required':
                working = working[:s_idx + 1] + pattern
                p_idx += 1
                s_idx += len(pattern)
                working = topoff(working, s_idx)
            elif assessment == 'incompatible':
                working = working[:s_idx] + '.'
                s_idx += 1
                working = topoff(working, s_idx)
            elif assessment == ('compatible'):
                working = working[:s_idx] + pattern
                if s_idx + len(pattern) != len(original):
                    forks.append((s_idx, p_idx))
                s_idx += len(pattern)
                p_idx += 1
                working = topoff(working, s_idx)

        if p_idx == len(patterns):
            if s_idx < len(working):
                if '#' not in working[s_idx:]:
                    working = working[:s_idx] + '.' * (len(working) - s_idx)
                    options.append(working)
            else:
                options.append(working)
            if len(forks) != 0:
                s_idx, p_idx, working = walkback(forks, p_idx, working)
            else:
                break
    return options

def dist_to_patterns(dist):
    patterns = []
    for i, group in enumerate(dist):
        if i != len(dist) - 1:
            patterns.append('#' * group + '.')
        else:
            patterns.append('#' * group)
    return patterns


def check_compatibility(string, pattern):
    compatibility = all([x == y for x, y in zip(list(string), list(pattern)) if x !='?'])
    return compatibility

def assess(string, pattern):
    if pattern[-1] == '.':
        if re.match(r'.*#.*\..*', string[:-1]) or re.match(r'.*\..*#.*\..*', string):
            assessment = 'broken'
        else:
            if check_compatibility(string, pattern):
                if re.match(r'.*#.*\.$', string):
                    assessment = 'required'
                else:
                    assessment = 'compatible'
            else:
                assessment = 'incompatible'
    else:
        if re.match(r'.*#.*\..*', string[:-1]):
            assessment = 'broken'
        else:
            if check_compatibility(string, pattern):
                assessment = 'compatible'
            else:
                assessment = 'incompatible'
    return assessment




def main():

    # Get Part 1 rows
    rows = []
    with open('input12.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            result = re.split(r"[\s,]", line)
            rows.append(Row(result[0], [int(x) for x in result[1:]]))
    rows = tuple(rows)

    # print('Part 1 (brute force): ', brute_force(rows))


    # for row in rows:
    #     patterns = valid_patterns(row.layout, row.dist)

    # Expand Rows
    rows_expanded = tuple(expand_rows(rows))

    # Part 2 Brute Force
    # print('Part 2 (brute force): ', brute_force(rows_expanded))

    total_options = 0
    for row in rows:
        total_options += len(walk_through(row.layout, row.dist))
    print(total_options)

    total_options = 0
    for i, row in enumerate(rows_expanded):
        print(i)
        total_options += len(walk_through(row.layout, row.dist))
    print(total_options)



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


