import re
from collections import namedtuple
import sympy
import numpy as np

Stone = namedtuple('stone', ['px', 'py', 'pz', 'vx', 'vy', 'vz'])

def parse_input(file):
    stones = []
    with open(file) as f:
        for line in f.read().splitlines():
            px, py, pz, vx, vy, vz = re.findall(r"-?\d+", line)
            stones.append(Stone(int(px), int(py), int(pz), int(vx), int(vy), int(vz)))
    return stones

test = False
stones = parse_input('test.txt' if test else 'input.txt')
lowbound = 7 if test else 200000000000000
highbound = 27 if test else 400000000000000
results = dict()
for i in range(len(stones) - 1):
    for j in range(i + 1, len(stones)):
        a = stones[i]
        b = stones[j]
        if a.vx == 0 and b.vx == 0:
            results.update({(i,j): 'parallel'})
            continue
        elif a.vx == 0 and b.vx != 0:
            x = a.px
            y = b.vy/b.vx * x + b.py - b.vy/b.vx
        elif a.vx != 0 and b.vx == 0:
            x = b.px
            y = a.vy/a.vx * x + a.py - a.vy/a.vx
        elif a.vy/a.vx == b.vy/b.vx:
            results.update({(i, j): 'parallel'})
            continue
        else:
            x = (b.py - a.py + a.vy/a.vx * a.px - b.vy/b.vx * b.px) / (a.vy/a.vx - b.vy/b.vx)
            y = a.vy/a.vx * x + a.py - a.vy/a.vx * a.px
        c1 = (lowbound <= x <= highbound) and (lowbound <= y <= highbound)
        c2 = (x > a.px and a.vx > 0) or (x < a.px and a.vx < 0) or (y > a.py and a.vy > 0) or (y < a.py and a.vy < 0)
        c3 = (x > b.px and b.vx > 0) or (x < b.px and b.vx < 0) or (y > b.py and b.vy > 0) or (y < b.py and b.vy < 0)
        match (c1, c2, c3):
            case (1,1,1):
                results.update({(i, j): 'valid intersection'})
            case _:
                results.update({(i, j): 'invalid intersection'})
print('Part 1: ', len([k for k, v in results.items() if v == 'valid intersection']))

# Stole from here: https://www.reddit.com/r/adventofcode/s/sHpOdcwLp2
# Basic idea is (my rock is r, hailstone is h, time is t
# 1) r.pos + t[i] * r.vel = h[i].pos + t[i] * h[i].vel (we can do this for x, y, and z)
# 2) Looking at only one collision means 7 variables (rpx, rpy, rpz, rvx, rvy, rvz, t[i]) but only 3 equations
# 3) If we look at our rock against another hailstone, we'll have 8 variables (add t[i+1] and 6 equations)
# 4) Add yet another and we'll have 9 variables (add t[i+2]) and 9 equations, enough to solve the system


def day24_part2(file):
    with open(file) as f:
        array = np.array([line.replace('@', ',').split(',') for line in f.read().splitlines()], int)
    p, v, t = (sympy.symbols(f'{ch}(:3)') for ch in 'pvt')
    equations = [
        array[i, j] + t[i] * array[i, 3 + j] - p[j] - v[j] * t[i]
        for i in range(3) for j in range(3)
    ]
    return sum(sympy.solve(equations, (*p, *v, *t))[0][:3])

part2 = day24_part2('input.txt')
print(f"Part 2: {part2}")
