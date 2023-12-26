import re
from collections import defaultdict
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent
INPUT_PATH = Path(SCRIPT_PATH, "input.txt")


# INPUT_PATH = Path(SCRIPT_PATH, "test.txt")

def parse_input(data):
    # Find the start point, and then split the input into a nested list and return the start point and the garden map
    data_list = data.splitlines()
    for idx, line in enumerate(data_list):
        start = re.search(r'S', line)
        if start is not None:
            start = (start.start(), idx)
            break
    data_list = [list(line) for line in data_list]
    return (start, data_list)


def possible_points(point, garden_map):
    # Loop over all possible directions, and yield each possible new point
    # Check the remainder of the point axis' divided by 131 to continue moving outward infinitely for part 2
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    for d in directions:
        new_point = (point[0] + d[0], point[1] + d[1])
        if garden_map[new_point[1] % 131][new_point[0] % 131] != '#':  # Make sure it wasn't a rock
            yield new_point


def bfs(point, garden_map, max_dist):
    # Use the Breadth first search to find the number of points hit each step, and return the dictionary with key of number of steps taken,
    # and value of number of points hit
    tiles = defaultdict(int)
    visited = set()
    queue = [(point, 0)]
    while queue:  # End when the queue is empty
        curr_point, dist = queue.pop(0)
        if dist == (max_dist + 1) or curr_point in visited:  # Don't include points that have already been visited
            continue

        tiles[dist] += 1
        visited.add(curr_point)

        for next_point in possible_points(curr_point, garden_map):  # Loop over possible points and add to queue
            queue.append((next_point, (dist + 1)))
    return tiles


def calculate_possible_spots(start, garden_map, max_steps):
    # Get the output from bfs, and then return the sum of all potential stopping points in the tiles output based on even or odd numbers
    tiles = bfs(start, garden_map, max_steps)
    return sum(amount for distance, amount in tiles.items() if distance % 2 == max_steps % 2)


def quad(y, n):
    # Use the quadratic formula to find the output at the large steps based on the first three data points
    # [x0, x1, x2] = [0, 1, 2] which leads to this simplification
    a = (y[2] - (2 * y[1]) + y[0]) // 2
    b = y[1] - y[0] - a
    c = y[0]
    return (a * n ** 2) + (b * n) + c


def part1(parsed_data):
    # Max steps are 64
    return calculate_possible_spots(*parsed_data, 64)


def part2(parsed_data):
    # Calculate the first three data points for use in the quadratic formula, and then return the output of quad
    goal = 26501365
    # size = number of spaces along edge of tile.
    size = len(parsed_data[1])
    # edge = number of spaces from the center to the edge
    edge = size // 2

    # Probably not a coincidence that the target number of steps happens to be 65 + a multiple of 131,
    #   which means it lies on the outer edge of a tile. The assumption is that the number of possible spaces to end
    #   on increases at a predictable rate (quadratic rate). So if we can get the equation of the relationship, we can
    #   plug in the number of tiles we need to traverse ((target - 65)/131) to get the total number of possible spaces
    #   one could have landed on after that many tiles. If the target were mid-tile, this solution wouldn't work.
    #   It was obviously architected to be solved this way.

    #  1) Calculate the number of possible spaces at:
    #       tiles = 0 (steps = 65)
    #       tiles = 1 (steps = 65 + 131)
    #       tiles = 2 (steps = 65 + 131 + 131)
    y = [calculate_possible_spots(*parsed_data, (edge + i * size)) for i in range(3)]

    #  2) Calculate spaces for number of tiles traversed to reach target steps
    return quad(y, ((goal - edge) // size))


if __name__ == "__main__":
    with open(INPUT_PATH, "r") as f:
        parsed_data = parse_input(f.read())
    answer1 = part1(parsed_data)
    answer2 = part2(parsed_data)

    print("--- ANSWERS ---")
    print(f"PART1 - The elf could reach {answer1} garden plots")
    print(f"PART2 - The elf could reach {answer2} garden plots")