#!/usr/bin/python3

def uppercase(str):
    for i in str:
        if 'a' <= i <= 'z':
            print(f"{chr(ord(i) - 32)}", end="")
        else: print(f"{i}", end="")
