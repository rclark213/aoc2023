
import re

def expand_rows(rows):
    rows_expanded = []
    for layout, dist in rows:
        layout_new = '?'.join([layout] * 5)
        dist_new = dist * 5
        rows_expanded.append((layout_new, dist_new))
    return rows_expanded

def find_possible(text, nums):

    states = '.'
    for num in nums:
        states += '#' * num + '.'

    occupancy = {0:1} # State: number of travellers
    new_occupancy = {}

    for c in text:
        for state in occupancy:
            final_state = state + 1 == len(states)
            if c == '?':
                if not final_state:
                    new_occupancy[state + 1] = new_occupancy.get(state + 1, 0) + occupancy[state]
                if states[state] == '.':
                    new_occupancy[state] = new_occupancy.get(state, 0) + occupancy[state]

            elif c == ".":
                if state + 1 < len(states) and states[state + 1] == ".": # If the next state is a dot,
                    new_occupancy[state + 1] = new_occupancy.get(state + 1, 0) + occupancy[state] # Move travelers to next state
                if states[state] == ".": # If the current state is a dot (looping allowed)
                    new_occupancy[state] = new_occupancy.get(state, 0) + occupancy[state] #Copy the current travelers to current state

            elif c == "#":
                if state + 1 < len(states) and states[state + 1] == "#": # If next state is a #
                    new_occupancy[state + 1] = new_occupancy.get(state + 1, 0) + occupancy[state] # Move the travelers, don't copy

        occupancy = new_occupancy
        new_occupancy = {}
    return occupancy.get(len(states) - 1, 0) + occupancy.get(len(states) - 2, 0)

rows = []
with open('input12.txt') as f:
    lines = f.read().splitlines()
    for line in lines:
        result = re.split(r"[\s,]", line)
        rows.append((result[0], [int(x) for x in result[1:]]))
    rows = tuple(rows)

t = 0
for row in rows:
    t += find_possible(row[0], row[1])

print(t)

t=0
for row in expand_rows(rows):
    t += find_possible(row[0], row[1])

print(t)