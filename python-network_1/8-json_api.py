#!/usr/bin/python3
"""post a letter and print search result from json response"""

import sys
import requests


if __name__ == "__main__":
    q_value = sys.argv[1] if len(sys.argv) > 1 else ""
    response = requests.post(
        "http://0.0.0.0:5000/search_user",
        data={"q": q_value},
        headers={'cfclearance': 'true'}
    )

    try:
        data = response.json()
        if data:
            print("[{}] {}".format(data.get("id"), data.get("name")))
        else:
            print("No result")
    except ValueError:
        print("Not a valid JSON")
