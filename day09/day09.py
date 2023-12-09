import re


def diff_down(seq_in):
    seqs = [seq_in]
    while set(seqs[-1]) != {0}:
        seqs.append([y-x for x, y in zip(seqs[-1], seqs[-1][1:])])
    right_total = sum([seq[-1] for seq in seqs])
    left_total = 0
    for seq in seqs[-1::-1]:
        left_total = seq[0] - left_total
    return right_total, left_total


with open("input09.txt") as f:
    lines = f.read().splitlines()

part_1_sum = 0
part_2_sum = 0
for line in lines:
    seq_int = [int(x) for x in re.split(r" ", line)]
    part_1, part_2 = diff_down(seq_int)
    part_1_sum += part_1
    part_2_sum += part_2

print('Part 1: ', part_1_sum)
print('Part 2: ', part_2_sum)