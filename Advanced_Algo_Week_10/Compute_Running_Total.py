# Compute running total of a list [1,2,3,4]  Bonus: Use multiplications
lst = [1, 2, 3, 4]
running_total = []
total = 0
for n in lst:
    total += n
    running_total.append(total)
print(running_total)
