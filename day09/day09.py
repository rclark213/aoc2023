import re


def diff_down(seq_in):
    seq_list_down = [seq_in]
    at_zero = False
    print(seq_in)
    while not at_zero:
        seq_out = [None] * (len(seq_in) - 1)
        for i in range(len(seq_out)):
            seq_out[i] = seq_in[i+1] - seq_in[i]
        seq_list_down.append(seq_out)
        seq_in = seq_out
        if set(seq_out) == {0}:
            at_zero = True
    seq_list_up = seq_list_down[::-1]
    seq_list_up_rev = [seq[::-1] for seq in seq_list_up]
    for i in range(len(seq_list_up) - 1):
        current_caboose = seq_list_up[i][-1]
        next_caboose = seq_list_up[i+1][-1]
        new_caboose = next_caboose + current_caboose
        seq_list_up[i+1].append(new_caboose)
    part_1 = new_caboose
    for i in range(len(seq_list_up_rev) - 1):
        current_caboose = seq_list_up_rev[i][-1]
        next_caboose = seq_list_up_rev[i+1][-1]
        new_caboose = next_caboose - current_caboose
        seq_list_up_rev[i+1].append(new_caboose)
    part_2 = new_caboose
    return part_1, part_2


with open("input09.txt") as f:
    lines = f.read().splitlines()

part_1_sum = 0
part_2_sum = 0
for line in lines:
    seq_string = re.split(r" ", line)
    seq_int = [int(x) for x in seq_string]
    part_1, part_2 = diff_down(seq_int)
    part_1_sum += part_1
    part_2_sum += part_2

print('Part 1: ', part_1_sum)
print('Part 2: ', part_2_sum)