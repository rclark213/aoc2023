import re
import numpy as np
import copy


class Cube:

    def __init__(self, x, y, z):
        self.xyz = (x, y, z)
        self.x = x
        self.y = y
        self.z = z

class Space:

    def __init__(self, stack):
        x_max = max([block.end.x for k, block in stack.items()])
        y_max = max([block.end.y for k, block in stack.items()])
        z_max = max([block.end.z for k, block in stack.items()])
        self.occupation = np.zeros((x_max + 1, y_max + 1, z_max + 1), dtype='uint')
        for key, block in stack.items():
            self.occupation[block.start.x:block.end.x + 1, block.start.y:block.end.y + 1, block.start.z:block.end.z+1] = key

    def update(self, block_key, zshift):
        old = np.where(self.occupation == block_key)
        new = (old[0], old[1], old[2] - zshift)
        self.occupation[old] = 0
        self.occupation[new] = block_key


class Block:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.settled = False
        self.supporters = set()
        self.supportees = set()
        diff = (start.x == end.x, start.y == end.y, start.z == end.z)
        match diff:
            case (True, True, True):
                self.orientation = 'cube'
            case (False, True, True):
                self.orientation = 'x'
                if self.start.x > self.end.x:
                    self.start.x = end.x
                    self.end.x = start.x
            case (True, False, True):
                self.orientation = 'y'
                if self.start.y > self.end.y:
                    self.start.y = end.y
                    self.end.y = start.y
            case (True, True, False):
                self.orientation = 'z'
                if self.start.z > self.end.z:
                    self.start.z = end.z
                    self.end.z = start.z


def parse_input(file):
    with open(file) as f:
        raw = f.read().splitlines()
    stack = dict()
    for i, line in enumerate(raw):
        start_x, start_y, start_z, end_x, end_y, end_z = re.split(r"[,~]", line)
        stack.update({i+1: Block(Cube(int(start_x), int(start_y), int(start_z)), Cube(int(end_x), int(end_y), int(end_z)))})
    return stack

def drop_blocks(stack, oldspace):
    stack = stack.copy()
    space = copy.deepcopy(oldspace)
    block_keys = [keys for (keys, items) in sorted(stack.items(), key=lambda item: item[1].start.z)]
    for k in block_keys:
        if stack[k].start.z == 1:
            stack[k].settled = True
        else:
            z = stack[k].start.z
            while not stack[k].settled:
                z -= 1
                if z == 0:
                    stack[k].settled = True
                else:
                    for y in range(stack[k].start.y, stack[k].end.y + 1):
                        for x in range(stack[k].start.x, stack[k].end.x + 1):
                            if space.occupation[x, y, z] != 0:
                                stack[k].supporters.add(space.occupation[x, y, z])
                                stack[space.occupation[x, y, z]].supportees.add(k)
                    stack[k].settled = len(stack[k].supporters) > 0
            zshift = stack[k].start.z - (z + 1)
            stack[k].start.z -= zshift
            stack[k].start.xyz = (stack[k].start.x, stack[k].start.y, stack[k].start.z)
            stack[k].end.z -= zshift
            stack[k].end.xyz = (stack[k].end.x, stack[k].end.y, stack[k].end.z)
            space.update(k, zshift)
    return stack

def chain_reaction(stack):
    block_keys = reversed([keys for (keys, items) in sorted(stack.items(), key=lambda item: item[1].start.z)])
    chains = dict()
    for k in block_keys:
        dissolved = {k}
        if not stack[k].safe:
            chain_going = True
            level = [k]
            while chain_going:
                next_level = []
                for n in level:
                    for up in stack[n].supportees:
                        if stack[up].supporters <= dissolved:
                            dissolved.add(up)
                            if up in chains.keys():
                                dissolved.union(chains[up])
                            next_level.append(up)
                level = next_level.copy()
                if len(level) == 0:
                    chain_going = False
            dissolved.remove(k)
            chains.update({k: dissolved})
    return chains

def tag_blocks(stack):
    for k, block in stack.items():
        safe = True
        for supportee in block.supportees:
            safe = safe and len(stack[supportee].supporters) > 1
        stack[k].safe = safe

stack = parse_input('input.txt')
s = Space(stack)
new_stack = drop_blocks(stack, s)
tag_blocks(new_stack)


t = 0
for k, v in new_stack.items():
    if v.safe:
        t += 1
print(f"Part 1: {t}")

chains = chain_reaction(new_stack)
t = 0
for k, v in chains.items():
    t += len(v) if v else 0
print(f"Part 2: {t}")
