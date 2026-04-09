#!/usr/bin/python3
def max_integer(my_list=[]):
    if len(my_list) == 0:
        return None

    max_val = my_list[0]
    for n in my_list:
        if n > max_val:
            max_val = n
    return max_val
