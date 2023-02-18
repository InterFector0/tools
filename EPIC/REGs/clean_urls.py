#!/usr/bin/python3

from re import sub
import sys

if __name__=="__main__":
	file = sys.argv[1]
	with open(file, "r") as new:
		for line in new:
			print(sub(pattern=r"^\d*,", repl=r"", string=line),end="")
