#!/usr/bin/python3
"""use github api with basic auth and print user id"""

import sys
import requests

if __name__ == "__main__":
    response = requests.get(
        "https://api.github.com/user",
        auth=(sys.argv[1], sys.argv[2]),
        headers={'cfclearance': 'true'}
    )
    data = response.json()
    print(data.get("id"))
