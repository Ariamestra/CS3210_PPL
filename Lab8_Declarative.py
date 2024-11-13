# Maria Estrada
# Lab 8 - Declarative Program

# Slice ------------------------------------------
def slice_imperative(list, start, end):
    sliced_list = []
    for i in range(start, end):
        sliced_list.append(list[i])
    return sliced_list

def slice_declarative(list, start, end):
    return list[start:end]

num = [1, 2, 3, 4, 5]
print("Imperative Slice (1 - 4):", slice_imperative(num, 1, 4))
print("Declarative Slice (1 - 4):", slice_declarative(num, 1, 4))

# Slice Output-------------------------------
'''
Imperative Slice (1 - 4): [2, 3, 4]
Declarative Slice (1 - 4): [2, 3, 4]
'''


# Search -----------------------------------------
def search_imperative(list, target):
    for item in list:
        if item == target:
            return True
    return False

def search_declarative(list, target):
    return target in list

num = [1, 2, 3, 4, 5]
print("Imperative Search for 3:", search_imperative(num, 3))
print("Declarative Search for 3:", search_declarative(num, 3))
print("Imperative Search for 6:", search_imperative(num, 6))
print("Declarative Search for 6:", search_declarative(num, 6))

# Search Output-------------------------------------------------
'''
Imperative Search for 3: True
Declarative Search for 3: True
Imperative Search for 6: False
Declarative Search for 6: False
'''