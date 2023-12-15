def find_mirror_index(grid):
    for i in range(1, len(grid)):
        top_half = grid[:i][::-1]
        bottom_half = grid[i:]

        total_mismatches = 0
        for top_row, bottom_row in zip(top_half, bottom_half):
            for (top_char, bottom_char) in zip(top_row, bottom_row):
                if top_char != bottom_char:
                    total_mismatches += 1
        if total_mismatches == 1:
            return i

    return 0


with open("input.txt", "r") as file:
    blocks = file.read().split("\n\n")

ans = 0
for block in blocks:
    grid = block.splitlines()

    row_index = find_mirror_index(grid)
    ans += row_index * 100

    transposed_grid = list(zip(*grid))
    column_index = find_mirror_index(transposed_grid)
    ans += column_index

print(ans)