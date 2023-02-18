#!/usr/bin/python3

import subprocess
import pandas as pd

def read():
    bashCommand = f"ls folder"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    ls = str(output).split("\\n")
    ls.remove("'")
    ls[0] = ls[0][2:]
    final = []
    for file in ls:
        bashCommand = f"cat folder/{file}"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        lis = str(output).split("\\n")
        for i in lis:
            if i != "'" and "Total Websites" not in i:
                final.append(i if i[:2] != "b'" else i[2:])
    return ls,final

def write(lis):
    finn = []
    with open('known_urls.txt', 'a+') as f:
        with open('known_urls.txt',"r") as fi:
            data = fi.readlines()
        for i in lis:
            if i+"\n" not in data:
                f.write(i+"\n")
                finn.append(i)
    return finn


args, urls = read()
new_urls = write(urls)
print(new_urls)
for key in args:
    key = key[:-4]
    bashCommand = f"sherlock -fo folder {key}"    
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

args, urls = read()
new_urls = write(urls)
for url in new_urls:
    print(url)
