#!/usr/bin/python
import pickle
ntdict = {'Accession':'Gene description'}

with open("nt.list",'r') as f:
    for line in f:
        line = line.rstrip()
        entry = line.split("\t")
        fullacc=entry[0].split(".")
        newentry={fullacc[0]:entry[1]} 
        ntdict.update(newentry)

with open("nt.pickle", 'wb') as handle:
    pickle.dump(ntdict, handle, protocol=pickle.HIGHEST_PROTOCOL)
