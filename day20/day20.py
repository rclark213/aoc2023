import re
from collections import namedtuple
import math

Pulse = namedtuple(typename='Pulse', field_names=['src', 'dest', 'sig', 'priority'])

class Coordinator:

    def __init__(self):
        self.queue = []
        self.pulse_count = [0,0]
        self.priority_level = 0

    def queue_up(self, pulse):
        self.queue.append(pulse)

    def process_queue(self, i):
        while len(self.queue) > 0:
            modules.get(self.queue[0].dest).receive(self.queue[0])
            self.pulse_count[self.queue[0].sig] += 1
            if self.queue[0].dest == 'rx' and self.queue[0].sig == 0:
                print(f"rx triggered with low signal at i = {i}")
            self.queue.pop(0)

class Button:

    def __init__(self, id='button'):
        self.id = id

    def press(self, i):
        pulse_out = Pulse(self.id, 'broadcaster', 0, 0)
        coordinator.queue_up(pulse_out)
        coordinator.process_queue(i)


class Broadcaster:

    def __init__(self, receivers, id='broadcaster'):
        self.receivers = receivers
        self.id = id

    def receive(self, pulse_in):
        for receiver in self.receivers:
            pulse_out = Pulse(self.id, receiver, pulse_in.sig, pulse_in.priority + 1)
            coordinator.queue_up(pulse_out)


class FlipFlop: # %

    def __init__(self, receivers, id):
        self.on = False
        self.receivers = receivers
        self.id = id

    def receive(self, pulse_in):
        if pulse_in.sig == 0:
            self.on = not self.on
            for receiver in self.receivers:
                pulse_out = Pulse(self.id, receiver, 1 if self.on else 0, pulse_in.priority + 1)
                coordinator.queue_up(pulse_out)


class Conjunction:

    def __init__(self, receivers, id):
        self.receivers = receivers
        self.senders = dict()
        self.id = id
        self.on = False
        self.cycles = set()
        self.final_node = False

    def receive(self, pulse_in):
        self.senders[pulse_in.src] = pulse_in.sig
        if self.final_node and any(self.senders.values()) and len(self.cycles) < 4:
            self.cycles.add(i)
            if len(self.cycles) == 4:
                self.cycles = tuple(self.cycles)
                print('Part 2: ', math.lcm(*self.cycles))


        self.on = all(self.senders.values())
        for receiver in self.receivers:
            if self.on:
                pulse_out = Pulse(self.id, receiver, 0, pulse_in.priority + 1)
            else:
                pulse_out = Pulse(self.id, receiver, 1, pulse_in.priority + 1)
            coordinator.queue_up(pulse_out)

    def find_senders(self):
        for module in modules.values():
            if self.id in module.receivers:
                self.senders.update({module.id: 0})

class Output:

    def __init__(self, id):
        self.id = id

    def receive(self, pulse_in):
        pass



def parse_input(file):
    modules = dict()
    with open(file) as f:
        lines = f.read().splitlines()

    for line in lines:
        left, right = re.match(r"(.*) -> (.*)", line).groups()
        receivers = re.findall(r"[a-z]+", right)
        if left == 'broadcaster':
            modules.update({"broadcaster": Broadcaster(receivers)})
        else:
            if left[0] == '%':
                modules.update({left[1:]: FlipFlop(receivers, left[1:])})
            elif left[0] == '&':
                modules.update({left[1:]: Conjunction(receivers, left[1:])})
                if 'rx' in receivers:
                    modules[left[1:]].final_node = True


    return modules

def get_ancestry(module, lvl=0):
    if lvl > 4:
        return None
    ancestry = [(module.id, type(module))]
    for name, m in modules.items():
        if hasattr(m, 'receivers'):
            if module.id in m.receivers:
                level = lvl + 1
                ancestry.append(get_ancestry(m, level))
    return ancestry

coordinator = Coordinator()
modules = parse_input('input.txt')
added_modules = dict()
for module in modules.values():
    if type(module) is Conjunction:
        module.find_senders()
    for receiver in module.receivers:
        if receiver not in modules.keys():
            added_modules.update({receiver: Output(id=receiver)})
modules.update(added_modules)

button = Button()
for i in range(1, 10000):
    button.press(i)

rx_ancestry = get_ancestry(modules['rx'], lvl=0)

print(f'Part 1: {coordinator.pulse_count[0] * coordinator.pulse_count[1]}')
print('')