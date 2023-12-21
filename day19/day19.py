import re
from collections import namedtuple
import portion as P

Stage = namedtuple(typename='Stage', field_names=['key', 'r', 'r_inv', 'dest'])

def check_rule(rule, gizmo):
    if '>' in rule:
        key, limit, dest = re.match(r"([xmas])>(\d+):(.+)", rule).groups()
        return gizmo.get(key) > int(limit), dest
    elif '<' in rule:
        key, limit, dest = re.match(r"([xmas])<(\d+):(.+)", rule).groups()
        return gizmo.get(key) < int(limit), dest
    else:
        return True, rule

def process_gizmo(gizmo, workflow, keep=True):
    k = keep
    dest = ''
    if workflow == 'A':
        dest = 'A'
        if keep:
            A.append(gizmo)
    elif workflow == 'R':
        dest = 'R'
        if keep:
            R.append(gizmo)
    else:
        for rule in workflows.get(workflow):
            passed, dest = check_rule(rule, gizmo)
            if passed:
                dest = process_gizmo(gizmo, dest, k)
                break
    return dest

A = []
R = []

with open('input.txt') as f:
    lines = f.read().splitlines()

workflows = {}
gizmos = []
for line in lines:
    if len(line) > 0:
        if line[0] != '{':
            wf_name, program = re.match(r"([a-z]+)\{(.+)}", line).groups()
            rules = program.split(',')
            workflows.update({wf_name: rules})
        elif line[0] == '{':
            keys = ['x', 'm', 'a', 's']
            values = re.match(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", line).groups()
            values = [int(v) for v in values]
            gizmos.append(dict(zip(keys, values)))

for gizmo in gizmos:
    process_gizmo(gizmo, 'in')

accepted_total = 0
for gizmo in A:
    accepted_total += gizmo['x'] + gizmo['m'] + gizmo['a'] + gizmo['s']

print(f'Total: {accepted_total}')

# Part 2

full_range = P.closed(1,4000)

queues = {}
for wf, rules in workflows.items():
    stages = []
    for rule in rules:
        if '<' in rule or '>' in rule:
            key, op, limit, dest = re.match(r"([xmas])([><])(\d+):(.+)", rule).groups()
            limit = int(limit)
            r = P.closedopen(1, limit) if op == '<' else P.openclosed(limit, 4000)
            r_inv = full_range - r
            stages.append(Stage(key, r, r_inv, dest))
        else:
            dest = rule
            stages.append(Stage(None, None, None, dest))
    queues.update({wf: stages})


##########################

rdict = {
    'x': P.closed(1,4000),
    'm': P.closed(1,4000),
    'a': P.closed(1,4000),
    's': P.closed(1,4000)
}

A_rdicts = []
R_rdicts = []

def build_ranges(rdict, queue):
    for i, stage in enumerate(queues[queue]):
        if stage.r:
            rdict_fork = rdict.copy()
            rdict_fork.update({stage.key: rdict[stage.key] & stage.r})
            if stage.dest == 'A':
                A_rdicts.append(rdict_fork)
            elif stage.dest == 'R':
                R_rdicts.append(rdict_fork)
            else:
                build_ranges(rdict_fork, stage.dest)
            rdict.update({stage.key: rdict[stage.key] & stage.r_inv})
        else:
            if stage.dest == 'A':
                A_rdicts.append(rdict)
            elif stage.dest == 'R':
                R_rdicts.append(rdict)
            else:
                build_ranges(rdict, stage.dest)

def interval_length(interval):
    left = interval.lower - 1 if interval.left == P.CLOSED else interval.lower
    right = interval.upper if interval.right == P.CLOSED else interval.upper - 1
    length = right - left
    return length

build_ranges(rdict, 'in')

t = 0
for r in A_rdicts:
    prod = 1
    for key, rng in r.items():
        prod = prod * interval_length(rng)
    t += prod

print('Part 2 (new Method)', t)



