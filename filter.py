# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import argparse



#Gets number of bad passwords
def getBadPW(dict):
    with open(dict) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#Handles the args
parser = argparse.ArgumentParser(description='Bloom Filter')

parser.add_argument('-d', action="store", default="dictionary.txt",dest='dict')
parser.add_argument('-i', action="store", default="input.txt",dest='inp')
parser.add_argument('-o', nargs = '*', action="store",dest='out', default=["output3.txt","output5.txt"])
args = parser.parse_args()

print(getBadPW(args.dict))
print(args.dict)
print(args.inp)
print(args.out)