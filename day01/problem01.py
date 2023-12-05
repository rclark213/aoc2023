import re
import logging

logging.basicConfig(filename='..\advent2023.log', filemode="w", format='%(levelname)s - %(message)s', level=logging.DEBUG)


def log_vars(vars):
    for k, v in vars.items():
        logging.debug(f"{k}: {v}")


# PART 1

logging.debug('PART 1 +++++++++++++')

with open("input01.txt") as file:
    last_line = False
    total = 0
    current_line = 0
    while not last_line:
        current_line += 1
        line_text = file.readline()
        if line_text != '':
            ints = re.findall('[0-9]', line_text)
            value = int(ints[0] + ints[-1])
            total += value
            log_vars({'current_line': current_line, 'ints': ints, 'value': value, 'total': total})
        else:
            last_line = True
            print('Part 1 Total: ', total)

# PART 2

logging.debug('Part 2 ++++++++++++++++++++')

int_words = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

int_words_rev = {k[::-1]: v for k, v in int_words.items()}

with open("input01.txt") as file:
    last_line = False
    total = 0
    forward_pattern = r'[0-9]|'+'|'.join(int_words.keys())
    reverse_pattern = r'[0-9]|'+'|'.join(int_words_rev.keys())
    current_line = 0
    while not last_line:
        current_line += 1
        line_text = file.readline()
        if line_text != '':
            forward_integers = re.findall(forward_pattern, line_text)
            forward_integers_dig = [int_words.get(x) if x in int_words.keys() else x for x in forward_integers]

            reverse_integers = re.findall(reverse_pattern, line_text[::-1])
            reverse_integers_dig = [int_words_rev.get(x) if x in int_words_rev.keys() else x for x in reverse_integers]

            value = int(forward_integers_dig[0] + reverse_integers_dig[0])
            total += value

            log_vars({'current_line': current_line,
                      'forward_integers': forward_integers, 'forward_integers_dig': forward_integers_dig,
                      'reverse integers': reverse_integers, 'reverse_integers_dig': reverse_integers_dig,
                      'value': value, 'total': total
                      })

        else:
            last_line = True
            print('Part 2 Total: ', total)


