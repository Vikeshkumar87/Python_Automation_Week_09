# Write the program to find the largest number from the list of numbers without build in functions.

list_of_numbers = [3, 5, 2, 8, 1,10,30,100,90, 200, 400, 500, 600, 700, 800, 900, 1000]
# Initialize the largest number to the first element of the list
largest_number = list_of_numbers[0]

# Iterate through the list to find the largest number
for number in list_of_numbers:
    if number > largest_number:
        largest_number = number

print("The largest number is:", largest_number)
# ouput:The largest number is: 1000