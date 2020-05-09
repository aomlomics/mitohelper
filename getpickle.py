#!/usr/bin/python

import pickle
import re

import sys
import os.path
from os import path

with open("/scratch1/jslim/nt.pickle", 'rb') as handle:
    NCBI = pickle.load(handle)

outfile="/scratch1/jslim/mitofish.genes"
nohit=0
count=0
length=(len(NCBI))

if path.exists(outfile) :
    sys.exit("Error: Output file exists! Please rename output file and try again!")

output=open(outfile,'a')

print("==== Searching... ====")

with open("/scratch1/jslim/mitofish.accession",'r') as infile:
    for inline in infile:
        inline = inline.rstrip()
        count +=1
        if inline in NCBI:
            output.write("%s#%s\n" % (inline,NCBI[inline]))
        elif inline not in NCBI:
            output.write("%s#No hit found!\n" % inline)
            print("%s#No hit found!" % inline)
            nohit +=1
            
output.close()

print ("==== Run complete! ===")
print ("Total: %d accession numbers" % count)
print ("No hits for %d input accession numbers!" % nohit)
