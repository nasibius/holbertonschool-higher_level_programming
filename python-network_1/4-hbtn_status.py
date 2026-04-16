#!/usr/bin/python3
"""get intranet status with requests"""
import requests


if __name__ == "__main__":
    r = requests.get("https://intranet.hbtn.io/status",
                     headers={"cfclearance": "true"})
    print("Body response:")
    print("\t- type: {}".format(type(r.text)))
    print("\t- content: {}".format(r.text))
