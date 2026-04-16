#!/usr/bin/python3
"""post email and print response body"""
import sys
import urllib.parse
import urllib.request


if __name__ == "__main__":
    data = urllib.parse.urlencode({"email": sys.argv[2]}).encode("ascii")
    req = urllib.request.Request(sys.argv[1], data=data)
    with urllib.request.urlopen(req) as response:
        print(response.read().decode("utf-8"))
