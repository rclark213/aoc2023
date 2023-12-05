import re
import numpy as np
from matplotlib import pyplot as plt

whitelist = '0123456789.'

with open('input03.txt') as f:
    lines = f.read().splitlines()  # List with a string for every line
    lines = [list(line) for line in lines]  # Break down lines into characters
    raw = np.pad(np.array(lines), 1, 'constant', constant_values='.')  # Create a numpy array, padded with periods
    symbol_mask = np.vectorize(lambda t: t not in whitelist)(raw)  # Numpy array where symbol locations are marked True
    R, C = np.where(symbol_mask)  # Row/Column locations of symbols
    marked = np.copy(raw)  # Copy of original padded text array
    for r, c in zip(R, C):  # Zip the rows and columns, iterate over them
        marked[r-1:r+2, c] = 'X'  # Put an X at, above, and below the symbol to break up the numbers
    raw_string = ''.join(raw.flatten())  # Flatten to 1D
    marked_string = ''.join(marked.flatten())  # Flatten to 1D
    all_parts = [int(x) for x in re.findall(r"\d+", raw_string)]  # All integers found in the original
    non_parts = [int(x) for x in re.findall(r"(?<=\.)\d+(?=\.)", marked_string)]  # All integers found in the altered version
    sum_all_parts = sum(all_parts)  # Sum of all potential parts
    sum_non_parts = sum(non_parts)  # Sum of invalid parts (parts not touching symbols)

    print('Sum of all potential parts: ', sum_all_parts)
    print('Sum of invalid parts: ', sum_non_parts)
    print('Difference (Sum of valid parts): ', sum_all_parts - sum_non_parts)

    # Part 2:

    part_map = np.zeros_like(raw, dtype='int')  # Initialize with zeros, same size as raw character array
    matches = re.finditer(r"\d+", raw_string)  # Find all locations and values of parts
    part_values = [0]  # Value of parts (integer that appears in raw array)
    for i, match in enumerate(matches):
        part_map.flat[match.start():match.end()] = i+1  # At every part location, the value is replaced with the 1-indexed index of the part (e.g. part # 42 has a value of 175, so [1, 7, 5] replaced with [42, 42, 42].
        part_values.append(int(match.group()))  # Populate part_values with actual value found through regex.

    R, C = np.where(raw == '*')  # Rows/columns of *'s
    gear_ratio_total = 0
    for r, c in zip(R, C):
        surrounding_coords = ([r-1, r-1, r-1, r, r, r+1, r+1, r+1], [c-1, c, c+1, c-1, c+1, c-1, c, c+1])  # Coordinates of surrounding 8 elements
        adj_parts_idx = list(set([x for x in part_map[surrounding_coords] if x > 0]))  # Find all unique part numbers around *
        if len(adj_parts_idx) == 2:  # If it touches exactly two parts
            gear_ratio_total += np.prod([part_values[x] for x in adj_parts_idx])  # Use the part numbers to multiply the part values and add to the total gear ratio


    print('Total Gear Ratio: ', gear_ratio_total)




print('end')



