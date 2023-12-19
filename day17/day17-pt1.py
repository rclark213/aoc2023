import sys

# Read the puzzle input
with open('input.txt') as file_desc:
    raw_file = file_desc.read()
# Trim whitespace on either end
raw_file = raw_file.strip()

# Parse into rows
grid_rows = raw_file.split("\n")

# Parse into numbers
grid = [[int(x) for x in row] for row in grid_rows]

# Calculate size of grid (we assume a square grid)
height = len(grid)
width = len(grid[0])

# Find the ending state
end_x = width - 1
end_y = height - 1

# Initialize data structures
state_queues_by_cost = {} # list of states sorted by the cost (g cost)
seen_cost_by_state = {}


def move_and_add_state(cost, x, y, dx, dy, distance):
    # Update the direction
    x += dx
    y += dy

    # Do bounds checking
    if x < 0 or y < 0:
        return
    if x >= width or y >= height:
        return

    # Calculate the cost of stepping on this square
    new_cost = cost + grid[y][x]

    # Did we find the end?
    if x == end_x and y == end_y:
        # Display our cost and early exit!
        print(">>>", new_cost, "<<<")
        sys.exit(0)

    # Create the state
    state = (x, y, dx, dy, distance)

    # Have we seen this state before?
    if state not in seen_cost_by_state:
        # Save the state to visit later
        state_queues_by_cost.setdefault(new_cost, []).append(state)

        # Mark the state as seen
        seen_cost_by_state[state] = new_cost


# We don't know which way we'll start, so try both
# The instructions say to ignore the starting cost
move_and_add_state(cost=0, x=0, y=0, dx=1, dy=0, distance=1)
move_and_add_state(cost=0, x=0, y=0, dx=0, dy=1, distance=1)

# Iterate till we find the exit
while True:

    # Find the horizon of our search, the states with the lowest cost
    # All future states will have at least this value, so we can just pop
    # Note: this assumes all grid values are positive!

    # Get lowest cost
    current_cost = min(state_queues_by_cost.keys())

    # Get all states at that cost
    next_states = state_queues_by_cost.pop(current_cost)

    # Process each state
    for state in next_states:

        # Break out the state variables
        (x, y, dx, dy, distance) = state

        # Perform the left and right turns
        move_and_add_state(cost=current_cost, x=x, y=y, dx=dy, dy=-dx, distance=1)
        move_and_add_state(cost=current_cost, x=x, y=y, dx=-dy, dy=dx, distance=1)

        if distance < 3:
            move_and_add_state(cost=current_cost, x=x, y=y, dx=dx, dy=dy, distance=distance + 1)

        print(len(state_queues_by_cost))