import itertools

cycle = itertools.cycle(['A', 'B', 'C'])

for _ in range(8):
    print(next(cycle))
