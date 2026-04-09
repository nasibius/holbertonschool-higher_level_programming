#!/usr/bin/python3
def print_matrix_integer(matrix=[[]]):
    for row in matrix:
        for j in range(len(row)):
            if j != 0:
                print(" ", end="")
            print("{:d}".format(row[j]), end="")
        print()
