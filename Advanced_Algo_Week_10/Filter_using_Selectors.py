# Filters ['a', 'b', 'c', 'd'] using selectors [1,0,1,0].
list1 = ['a', 'b', 'c', 'd']
selectors = [1, 0, 1, 1]
# Filter the list using selectors. The expression "item for item, selector in zip(list1, selectors) if selector" means:
# For each pair of (item, selector) obtained by zipping list1 and selectors, include the item in the filtered list if the selector is truthy.

filtered_list = [item for item, selector in zip(list1, selectors) if selector]
print(filtered_list)