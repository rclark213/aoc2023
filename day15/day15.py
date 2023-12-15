import re

# Create a dictionary of boxes 0 through 255

boxes = {i: [] for i in range(256)}

# Functions for Part 2 - placing a lens in a box, or removing a lens from a box

def place(label, f, box):
    labels = [lens[0] for lens in boxes[box]]
    if label in labels:
        boxes[box][labels.index(label)] = (label, f)
    else:
        boxes[box].append((label, f))

def remove(label, box):
    labels = [lens[0] for lens in boxes[box]]
    if label in labels:
        boxes[box].pop(labels.index(label))

# Split the line into string sequences separated by commas

with open('input.txt') as f:
    txt = f.read()
    # txt = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
    seqs = re.split(r',',txt)

# Function for getting the hash value of a string

def h(s):
    val = 0
    for c in s:
        val = ((val + ord(c)) * 17) % 256
    return val

# Part 1

t = 0
for seq in seqs:
    val = h(seq)
    t += val

print('Part 1: ', t)

# Part 2

# Get the label, operation, and focal length for each sequence
# Hash the label to get the box key
# Perform the intended operation

for seq in seqs:
    label, operation, f = re.match(r'([a-z]+)([-=])(\d*)', seq).groups()
    box = h(label)
    if operation == '=':
        place(label, int(f), box)
    elif operation == '-':
        remove(label, box)

# Keep a running power value
# For each box, for each lens, calculate the power and add to total

power = 0
for box in boxes.items():
    for i, lens in enumerate(box[1]):
        power += (box[0] + 1) * (i+1) * lens[1]


print('Power: ', power)





