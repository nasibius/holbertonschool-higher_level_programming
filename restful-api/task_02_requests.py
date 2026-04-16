#!/usr/bin/python3
"""fetch and process posts from jsonplaceholder"""
import csv
import requests

URL = "https://jsonplaceholder.typicode.com/posts"

def fetch_and_print_posts():
    """fetch posts and print status code and titles."""
    response = requests.get(URL)
    print("Status Code: {}".format(response.status_code))
    if response.status_code == 200:
        for post in response.json():
            print(post.get("title"))


def fetch_and_save_posts():
    """fetch posts and save selected fields to posts.csv."""
    response = requests.get(URL)
    if response.status_code == 200:
        posts = [
            {
                "id": post.get("id"),
                "title": post.get("title"),
                "body": post.get("body")
            }
            for post in response.json()
        ]
        with open("posts.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "title", "body"])
            writer.writeheader()
            writer.writerows(posts)
