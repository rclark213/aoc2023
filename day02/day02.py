import re

test_text = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n\
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n\
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n\
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n\
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"

bag = {
    "red": 12,
    "green": 13,
    "blue": 14
}

# Part 1
running_total = 0
test_lines = test_text.splitlines()


with open("input02.txt") as file:
    lines = file.read().splitlines()
    for line_text in lines:
        game_possible = True
        line_parts = re.split(r"[:;]", line_text)
        for line_part in line_parts[1:]:
            for color in ['red', 'green', 'blue']:
                regex = r"(\d+) " + color
                try:
                    if int(re.findall(regex, line_part)[0]) > bag.get(color):
                        game_possible = False
                except:
                    pass
        if game_possible:
            running_total += int(re.findall(r"\d+", line_parts[0])[0])
            print(running_total)

print(running_total)

# Part 2

with open("input02.txt") as file:
    lines = file.read().splitlines()
    running_total = 0
    for line_text in lines:
        min_dice = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        line_parts = re.split(r"[:;]", line_text)
        for line_part in line_parts[1:]:
            for color in ['red', 'green', 'blue']:
                regex = r"(\d+) " + color
                try:
                    pulled_num = int(re.findall(regex, line_part)[0])
                    if pulled_num > min_dice.get(color):
                        min_dice[color] = pulled_num
                except:
                    pass

        (r, b, g) = min_dice.values()
        running_total += r * b * g
        print(running_total)