import re
from itertools import cycle
from collections import OrderedDict
import time
import math

with open("input08.txt") as f:
    lines = f.read().splitlines()


directions = cycle([int(x) for x in list(lines[0].replace("L", "0").replace("R", "1"))])
node_map = OrderedDict()

for line in lines[2:]:
    (node, left, right) = re.findall(r"(\w\w\w)", line)
    node_map.update({node: (left, right)})

nodes = list(node_map.keys())
choices = []
for node in list(node_map.values()):
    choices.append((nodes.index(node[0]), nodes.index(node[1])))

start = nodes.index('AAA')
target = nodes.index('ZZZ')



current_node = start
print(current_node)
steps = 0
for direction in directions:
    current_node = choices[current_node][direction]
    steps += 1
    if current_node == target:
        break

print('Steps to ZZZ: ', steps)

# Part 2:

starts = [i for i, node in enumerate(nodes) if node[-1] == 'A']
targets = set([i for i, node in enumerate(nodes) if node[-1] == 'Z'])
print(starts)
print(targets)

# Naive approach:

# current_nodes = starts
# steps = 0
# for direction in directions:
#     current_nodes = [choices[node][direction] for node in current_nodes]
#     steps += 1
#     if steps % 1000000 == 0:
#         print(steps)
#     if set(current_nodes) <= targets:
#         break

# Better approach:
intervals = []
for start in starts:
    steps = 0
    current_node = start
    for direction in directions:
        current_node = choices[current_node][direction]
        steps += 1
        if current_node in targets:
            intervals.append(steps)
            print(steps)
            print()
            break

steps_to_convergence = math.lcm(*intervals)


print('Steps to convergence: ', steps_to_convergence)