
import re

# Function to Expand Rows to 5X

def expand_rows(rows):
    rows_expanded = []
    for layout, dist in rows:
        layout_new = '?'.join([layout] * 5)
        dist_new = dist * 5
        rows_expanded.append((layout_new, dist_new))
    return rows_expanded

# Non-Deterministic Finite Automaton

def find_possible(text, nums):

    # Build a series of states that are all valid and building toward the accepted states
    # The states are based solely off of the group numbers
    # Example for group numbers (1,3):
    #       States:         .   #   .   #   #   #   .
    #       State Number:   0   1   2   3   4   5   6
    #       Accepted?       N   N   N   N   N   Y   Y
    # Dead states aren't tracked (e.g. in example above, an input # is provided for state 1)

    states = '.'
    for num in nums:
        states += '#' * num + '.'

    # Occupancy is a dictionary of {state number : number of travellers in that state}
    # Initial state is a dot with one traveller

    occupancy = {0:1}
    new_occupancy = {} # Updated throughout input processing then replaces occupancy

    for c in text: # For each character in the text
        for state in occupancy: # For each occupied state
            final_state = state + 1 == len(states) # Nothing happens to travellers already at the final state
            if c == '?':
                if not final_state: # As long as we're not at the final state, add travellers to the next state
                    new_occupancy[state + 1] = new_occupancy.get(state + 1, 0) + occupancy[state]
                if states[state] == '.': # A dot can always follow another and maintain the required pattern.
                    new_occupancy[state] = new_occupancy.get(state, 0) + occupancy[state]

            elif c == ".":
                if state + 1 < len(states) and states[state + 1] == ".":  # If the next state is a dot,
                    # Add travellers to next state
                    new_occupancy[state + 1] = new_occupancy.get(state + 1, 0) + occupancy[state]
                if states[state] == ".": # If the current state is a dot (looping allowed) # If current state is a dot
                    # Keep a copy of the travellers at the current state
                    new_occupancy[state] = new_occupancy.get(state, 0) + occupancy[state]

            elif c == "#":
                if state + 1 < len(states) and states[state + 1] == "#": # If next state is a #
                    # Travellers must move to the next state.
                    new_occupancy[state + 1] = new_occupancy.get(state + 1, 0) + occupancy[state]

        # Changing of the guard

        occupancy = new_occupancy
        new_occupancy = {}

        # Return the sum of travellers at the two states at the end of the line
        # n - 2 is the situation where the pattern was satisfied and ended on a #
        # n - 1 is the situation where the pattern was satisfied and ended on a .

    return occupancy.get(len(states) - 1, 0) + occupancy.get(len(states) - 2, 0)

rows = []
with open('input12.txt') as f:
    lines = f.read().splitlines()
    for line in lines:
        result = re.split(r"[\s,]", line)
        rows.append((result[0], [int(x) for x in result[1:]]))
    rows = tuple(rows)

# Part 1

t = 0
for row in rows:
    t += find_possible(row[0], row[1])

print(t)

# Part 2 (same as Part 1, but unfold the rows)

t=0
for row in expand_rows(rows):
    t += find_possible(row[0], row[1])

print(t)