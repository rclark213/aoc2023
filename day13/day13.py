import numpy as np
from pprint import pprint

with open('input.txt') as f:
    lines = f.read().splitlines()

mirrors = []
mirror = []
for line in lines:
    if line:
        mirror.append([int(x) for x in line.replace('.','0').replace('#', '1')])
    else:
        mirrors.append(np.array(mirror))
        mirror = []
if len(mirror) > 0:
    mirrors.append(np.array(mirror))

def symmetric(m, diff_idx):
    i = diff_idx + 1
    # Make sure line of sym is a horizontal line
    if i < m.shape[0] / 2:
        a = m[0:i, :]
        b = np.flipud(m[i:2 * i, :])
    elif i == m.shape[0] / 2:
        a = m[0:i, :]
        b = np.flipud(m[i:, :])
    elif i > m.shape[0] / 2:
        a = m[2 * i - m.shape[0]:i, :]
        b = np.flipud(m[i:, :])
    sym = True
    for j in range(a.shape[0] - 1):
        sym = sym and np.all(np.logical_not(np.logical_xor(a[j, :], b[j, :])))
    return sym




def find_symmetry(m, symtype='horz'):
    if symtype == 'horz':
        coef = 100
    elif symtype == ('vert'):
        coef = 1
    los = 0
    for i in range(1, m.shape[0]):
        if np.all(np.logical_not(np.logical_xor(m[i-1, :], m[i, :]))):
            if i < m.shape[0]/2:
                a = m[0:i, :]
                b = np.flipud(m[i:2*i, :])
            elif i == m.shape[0]/2:
                a = m[0:i, :]
                b = np.flipud(m[i:, :])
            elif i > m.shape[0]/2:
                a = m[2*i - m.shape[0]:i, :]
                b = np.flipud(m[i:, :])
            sym = True
            for j in range(a.shape[0]-1):
                sym = sym and np.all(np.logical_not(np.logical_xor(a[j,:], b[j,:])))
            if sym:
                los = i

                break
    if los != 0:
        score = coef * los
        print(f'{symtype} line found between {los - 1} and {los} with score of {score}')
    else:
        print('Transpose')
        los, score = find_symmetry(np.transpose(m), 'vert')
    return los, score

def find_smudge(m):
    rowdiff = np.sum(np.logical_xor(m[0:-1,:], m[1:,:]), axis=1)
    possible_loc = [x for x in rowdiff if x == 1]

    coldiff = np.sum(np.logical_xor(m[:, 0:-1], m[:, 1:]), axis=1)



def part1():
    tot = 0
    for i, mirror in enumerate(mirrors):
        print('Mirror', i)
        los, score = find_symmetry(mirror)
        tot += score
    return tot

print('Part 1: ', part1())

print('end')





