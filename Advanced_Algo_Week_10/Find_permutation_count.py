# Find all Permutations of length 3 from  [1,2,3,4] and count them.
from itertools import permutations

lst = [1, 2, 3, 4]
perm = list(permutations(lst, 3))
print(perm)
print("Count:", len(perm))

# Output: [(1, 2, 3), (1, 2, 4), (1, 3, 2), (1, 3, 4), (1, 4, 2), (1, 4, 3), (2, 1, 3), (2, 1, 4), (2, 3, 1), (2, 3, 4), (2, 4, 1), (2, 4,3), (3, 1, 2), (3, 1, 4), (3, 2, 1), (3, 2, 4), (3, 4, 1), (3, 4, 2), (4, 1, 2), (4, 1, 3), (4, 2, 1), (4, 2, 3), (4, 3, 1), (4,3, 2)]
# Count: 24