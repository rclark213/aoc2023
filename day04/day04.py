import re

# Part 1

with open('input04.txt') as f:
    lines = f.read().splitlines()  # List with a string for every line
    stack_value = 0  # Running point value total
    card_matches = []  # Number of matches for each card
    for line in lines:
        parts = re.split(r"[:|]", line)  # Split the line into 3 strings: [Card num, winning nums, my nums]
        winning_nums = set(re.findall(r"\d+", parts[1]))  # Set of winning nums
        my_nums = set(re.findall(r"\d+", parts[2]))  # Set of my nums
        num_of_matches = len(winning_nums.intersection(my_nums))  # Intersection of the two sets gives number of matches
        card_matches.append(num_of_matches)  # Tracked for Part 2
        ticket_value = 2 ** (num_of_matches - 1) if num_of_matches > 0 else 0
        stack_value += ticket_value
    print("Stack value: ", stack_value)

# Part 2

card_quants = [1] * len(card_matches)  # One copy of each card to start with
for i, card_val in enumerate(card_matches): # Go through the card matches
    card_quants[i+1:i+1+card_val] = [x + card_quants[i] for x in card_quants[i+1:i+1+card_val]]
print('Total Cards: ', sum(card_quants))