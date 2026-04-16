#!/usr/bin/python3
"""send a request to a url and print body or error code"""

import sys
import urllib.request
import urllib.error


if __name__ == "__main__":
    url = sys.argv[1]
    req = urllib.request.Request(url, headers={'cfclearance': 'true'})

    try:
        with urllib.request.urlopen(req) as response:
            print(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print("Error code: {}".format(e.code))
