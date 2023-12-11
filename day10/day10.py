import math
from collections import *
import numpy as np
from scipy.ndimage import label, generate_binary_structure

Neighbors = namedtuple('Neighbors', ['R', 'D', 'L', 'U'])

right_valid = '-7JS'
down_valid = '|LJS'
left_valid = '-FLS'
up_valid = '|F7S'

valid_dirs = {
    '|': 'UD',
    '-': 'LR',
    '7': 'LD',
    'L': 'UR',
    'F': 'DR',
    'J': 'LU',
}

opp_dir = {
    'R': 'L',
    'D': 'U',
    'L': 'R',
    'U': 'D'
}

# Looks right from current cell of the dir_arr. 'U' and 'D' logic worked for my input, but might need to be flipped otherwise.

def stretch(idx):
    for box in dir_arr[idx[0], idx[1]:]:
        if box != '':
            if box == 'O': # If it encounters the right edge of the array
                location = 'O'
            elif 'U' in box:
                location = 'O'
            elif 'D' in box:
                location = 'I'
            break
    return location


def shift(idx, direction): # Get neighbor index
    if direction == 'R':
        shifted_idx = (idx[0], idx[1]+1)
    if direction == 'D':
        shifted_idx = (idx[0] + 1, idx[1])
    if direction == 'L':
        shifted_idx = (idx[0], idx[1] - 1)
    if direction == 'U':
        shifted_idx = (idx[0] - 1, idx[1])
    return shifted_idx

def look_around(idx, arr): # R D L U
    nix = [(idx[0], idx[1]+1), (idx[0]+1, idx[1]), (idx[0], idx[1]-1), (idx[0]-1, idx[1])]
    neighbors = Neighbors(R=arr[nix[0]], D=arr[nix[1]], L=arr[nix[2]], U=arr[nix[3]])
    if neighbors.R in right_valid:
        next_spot = nix[0]
        pipetype = neighbors.R
        prev_spot = 'L'
    elif neighbors.D in down_valid:
        next_spot = nix[1]
        pipetype = neighbors.D
        prev_spot = 'U'
    elif neighbors.L in left_valid:
        next_spot = nix[2]
        pipetype = neighbors.L
        prev_spot = 'R'
    elif neighbors.U in left_valid:
        next_spot = nix[3]
        pipetype = neighbors.U
        previous_spot = 'D'
    return next_spot, pipetype, prev_spot

def keep_going(idx, prev_direction):
    possible = valid_dirs[arr[idx]]
    new_dir = possible.replace(prev_direction, '')
    next_space = shift(idx, new_dir)
    prev_direction = opp_dir[new_dir]
    return next_space, prev_direction


with open('input10.txt') as f:
    lines = f.read().splitlines()

charmap = [list(line) for line in lines]
arr = np.pad(np.array(charmap), 1, 'constant', constant_values='.') # Create the array and pad to avoid boundary issues
dir_arr = np.empty_like(arr,dtype='U2') # An array to track the direction I was moving in when adding the cell to the path
start = np.where(arr == 'S')
start = (start[0][0], start[1][0])

loc, character, prev_dir = look_around(start, arr) # My function is overkill. I thought I'd be generalizing it.
dir_arr[loc] = prev_dir
steps = [start, loc]
looped = False
while not looped:
    loc, prev_dir = keep_going(loc, prev_dir)
    dir_arr[loc] = prev_dir
    prior_dir = dir_arr[steps[-1]]
    if dir_arr[steps[-1]] != prev_dir:
        d = dir_arr[steps[-1]] + prev_dir
        dir_arr[steps[-1]] = d
    steps.append(loc)
    if loc == start:
        looped = True

if dir_arr[steps[0]] != dir_arr[steps[1]]:
    dir_arr[steps[0]] = dir_arr[steps[0]] + dir_arr[steps[1]][0]

# For debugging purposes:

path_arr = np.empty_like(dir_arr, dtype='U5')
for i, step in enumerate(steps):
    path_arr[step] = i

print('Part 1: ', math.floor(len(steps)/2))

# Creating a boolean array for group labeling

non_path_arr = np.ones_like(arr, dtype=bool)
r = [step[0] for step in steps]
c = [step[1] for step in steps]
non_path_arr[r,c] = False

# Find all RDLU contiguous groups. Each has a unique label integer in a new array.

label, num_features = label(non_path_arr)

# Prepping for Part 2

dir_arr[0, :] = 'O'
dir_arr[:, 0] = 'O'
dir_arr[-1, :] = 'O'
dir_arr[:, -1] = 'O'


io_arr = np.empty_like(dir_arr, dtype='U1') # Array where outside the path 'O' and inside the path 'I'
for lbl in range(1,num_features):
    members = np.where(label == lbl)
    location = stretch((members[0][0], members[1][0]))
    if location == 'I':
        io_arr[members] = location


print('Part 2: ', len(np.argwhere(io_arr == 'I')))






