import re
import math

# distance = speed * time_running
# speed = time_pressing * (1)
# total_time = time_pressing + time_running
# ---> time_running = total_time - time_pressing
# ---> distance = time_pressing * (total_time - time_pressing)
# ---> d = tp * T - tp^2
# ---> d/dt(d) = T - 2tp
# ---> 0 = T - 2tp
# ----> tp = T/2 (optimum pressing time)



with open('input06.txt') as f:
    lines = f.read().splitlines()
    times = [int(x) for x in re.findall(r"(\d+)", lines[0])]
    distances = [int(x) for x in re.findall(r"(\d+)", lines[1])]
    full_time = int(''.join(re.findall(r"(\d+)", lines[0])))
    full_distance = int(''.join(re.findall(r"(\d+)", lines[1])))

print(times)
print(distances)
solutions_prod = 1

for t, d in zip(times, distances):
    optimal_tb = int(t/2)
    tb1 = (t + math.sqrt(t**2 - 4*d))/2
    tb2 = (t - math.sqrt(t**2 - 4*d))/2
    tb_bounds = [math.ceil(min(tb1, tb2)), math.floor(max(tb1, tb2))]
    solutions = tb_bounds[1] - tb_bounds[0] + 1
    solutions_prod = solutions_prod * solutions

print("Part 1: ", solutions_prod)

tb1 = (full_time + math.sqrt(full_time ** 2 - 4 * full_distance)) / 2
tb2 = (full_time - math.sqrt(full_time ** 2 - 4 * full_distance)) / 2
tb_bounds = [math.ceil(min(tb1, tb2)), math.floor(max(tb1, tb2))]
solutions = tb_bounds[1] - tb_bounds[0] + 1

print("Part 2: ", solutions)


