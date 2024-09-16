# Lab 3 - Maria Estrada
# Due Sep 18
from functools import reduce

#1)Write a Python program to find the intersection (common elements) of two given arrays using Lambda.
array1 = [1, 2, 3, 4, 5]
array2 = [2, 4, 6, 8, 10]

intersection = list(filter( lambda x: x in array1, array2))

print("--------------Question 1---------------------")
print("Intersection:", intersection)

#2) Write a Python program to count the even and odd numbers in a given array of integers using Lambda.

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

evens = list(filter(lambda x: x % 2 == 0, numbers))
odds = list(filter(lambda x: x % 2 != 0, numbers))

print("--------------Question 2---------------------")
print("Even Number:", len(evens), "-", evens)
print("Odd Number:", len(odds), "-", odds)


#3)  Given a list of integers from 1 to 15, perform the following operations using lambda functions:
    #Use map() to add 5 to each number in the list.
    #Use filter() to keep only the numbers that are divisible by 3.
    #Use reduce() to find the sum of the remaining numbers.

int = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

num_plus_5 = list(map(lambda x: x+5, int))
print("--------------Question 3---------------------")
print("Numbers Plus 5:", num_plus_5)

div_by_3 = list(filter(lambda x: x % 3 == 0, num_plus_5))
print("Divisible by 3:", div_by_3)

# not_div_by_3 = int - div_by_3--------------------

sum_of_num = reduce(lambda x, y: x+y, not_div_by_3)
print("Sum of Numbers Divisible by 3:", sum_of_num)
print("--------------------------------------------")

