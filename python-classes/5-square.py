#!/usr/bin/python3
"""square class"""


class Square:
    """square"""
    def __init__(self, size=0):
        """init"""
        self.size = size

    @property
    def size(self):
        """size"""
        return self.__size

    @size.setter
    def size(self, value):
        """set size"""
        if not isinstance(value, int):
            raise TypeError("size must be an integer")
        if value < 0:
            raise ValueError("size must be >= 0")
        self.__size = value

    def area(self):
        """area"""
        return self.__size ** 2

    def my_print(self):
        """print square"""
        if self.__size == 0:
            print()
            return
        for _ in range(self.__size):
            print("#" * self.__size)
