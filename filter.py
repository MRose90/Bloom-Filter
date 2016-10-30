# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from bitarray import bitarray
from math import log
import argparse
import hashlib
glob_prob = .5


#Gets number of bad passwords
def getBadPW(dic):
    with open(dic) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#calculates the array size
#formula is solved from (1-e^(-kB/N))^k
#abs is taken to get positive values
def calcArraySize(B,k):
    return (int)(abs((k * B)/log(1-glob_prob**(1/k))))
   

#Sets both bloom filter bitarrays.    
def setArrays(bf3,bf5,dic):
    with open(dic) as f:
        for l in f:
            val = l.encode('utf-8')
            md5 = int(hashlib.md5(val).hexdigest(),16)
            sha224 = int(hashlib.sha224(val).hexdigest(),16)
            sha256 = int(hashlib.sha256(val).hexdigest(),16)
            sha384 = int(hashlib.sha384(val).hexdigest(),16)
            sha512 = int(hashlib.sha512(val).hexdigest(),16)
            bf3[md5%len(bf3)] = 1
            bf5[md5%len(bf5)] = 1
            bf3[sha512%len(bf3)] = 1
            bf5[sha512%len(bf5)] = 1
            bf3[sha384%len(bf3)] = 1
            bf5[sha384%len(bf5)] = 1
            bf5[sha256%len(bf5)] = 1
            bf5[sha224%len(bf5)] = 1
    return bf3,bf5
    
def testPassword(bf3,bf5,pw):
    bf3Bool = True
    bf5Bool = True
    md5 = int(hashlib.md5(pw).hexdigest(),16)
    sha224 = int(hashlib.sha224(pw).hexdigest(),16)
    sha256 = int(hashlib.sha256(pw).hexdigest(),16)
    sha384 = int(hashlib.sha384(pw).hexdigest(),16)
    sha512 = int(hashlib.sha512(pw).hexdigest(),16)
    if bf3[md5%len(bf3)] == 0 or bf3[sha512%len(bf3)] == 0 or bf3[sha384%len(bf3)] == 0:
        bf3Bool = False
    if bf5[md5%len(bf5)] == 0 or bf5[sha512%len(bf5)] == 0 or bf5[sha384%len(bf5)] == 0 or bf5[sha256%len(bf5)] == 0 or bf5[sha224%len(bf5)] == 0:
        bf5Bool = False
    return bf3Bool,bf5Bool
#Test a new password
def testPasswords(bf3,bf5,inp):
    bf3Bool = []
    bf5Bool = []
    with open(inp) as f:
        for l in f:
            i = l.encode('utf-8')
            bf3temp,bf5temp = testPassword(bf3,bf5,i)
            bf3Bool.append(bf3temp)
            bf5Bool.append(bf5temp)
    return bf3Bool,bf5Bool
#write to file
def writeFiles(out,bf3,bf5):
    print(out[0])
    print(out[1])
    f = open(out[0],'w')
    for v in bf3:    
        if v:
            f.write('maybe\n')
        else:
            f.write('no\n')
    f.close()
    f = open(out[1],'w')
    for v in bf5:    
        if v:
            f.write('maybe\n')
        else:
            f.write('no\n')
    f.close()
#Handles the args
parser = argparse.ArgumentParser(description='Bloom Filter')

parser.add_argument('-d', action="store", default="dictionary.txt",dest='dic')
parser.add_argument('-i', action="store", default="input.txt",dest='inp')
parser.add_argument('-o', nargs = '*', action="store",dest='out', default=["output3.txt","output5.txt"])
args = parser.parse_args()

numBadPW = getBadPW(args.dic)
bf3 = bitarray(calcArraySize(numBadPW,3))
bf5 = bitarray(calcArraySize(numBadPW,5))
for i in bf3:
    bf3[i] = 0
for i in bf5:
    bf5[i] = 0
bf3,bf5 = setArrays(bf3,bf5,args.dic)
bf3Bool, bf5Bool = testPasswords(bf3,bf5,args.inp)
writeFiles(args.out,bf3Bool,bf5Bool)
print(args.dic)
print(args.inp)
print(args.out)