#!/bin/bash
# get body size
curl -s "$1" | wc -c
