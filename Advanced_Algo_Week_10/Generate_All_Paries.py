# Generate ALL Pairs of [1,2] and ['A','B']
from itertools import product

list1 = [1, 2]
list2 = ['A', 'B']
all_pairs = list(product(list1, list2))
print(all_pairs)