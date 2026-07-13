# Find all 2-letter combinations from a given string "ABCD"
from itertools import combinations

string = "ABCD"
two_letter_combinations = list(combinations(string, 2))
print(two_letter_combinations)
