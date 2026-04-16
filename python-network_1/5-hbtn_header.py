#!/usr/bin/python3
"""send request and print x-request-id header value"""

import sys
import requests


if __name__ == "__main__":
    response = requests.get(sys.argv[1], headers={'cfclearance': 'true'})
    print(response.headers.get("X-Request-Id"))
