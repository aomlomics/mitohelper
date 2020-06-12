#!/usr/bin/python

import pickle
import sys
import os.path
from os import path

with open("nt.pickle", 'rb') as handle:
    NCBI = pickle.load(handle)

outfile="mitofish.genes"
nohit=0
count=0
length=(len(NCBI))

if path.exists(outfile) :
    sys.exit("Error: Output file exists! Please rename output file and try again!")

output=open(outfile,'a')

print("==== Searching... ====")

with open("mitofish.accession",'r') as infile:
    for inline in infile:
        inline = inline.rstrip()
        count +=1
        if inline in NCBI:
            output.write("%s\t%s\n" % (inline,NCBI[inline]))
        elif inline not in NCBI:
            output.write("%s\tNo hit found!\n" % inline)
            print("%s\tNo hit found!" % inline)
            nohit +=1
            
output.close()

print ("==== Run complete! ===")
print ("Total: %d accession numbers" % count)
print ("No hits for %d input accession numbers!" % nohit)
