#!/usr/bin/python3
import requests


with open("urls.txt", 'r') as f:
    Lines = f.readlines()
    for line in Lines:
        r = requests.get(line)
        for x in r.history:
            print(x.url)
        print(r.url)
