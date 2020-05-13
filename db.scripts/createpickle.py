#!/usr/bin/python
import pickle
ntdict = {'Accession':'Gene description'}

with open("/scratch1/jslim/nt.list",'r') as f:
    for line in f:
        line = line.rstrip()
        entry = line.split("#")
        fullacc=entry[0].split(".")
        newentry={fullacc[0]:entry[1]} 
        ntdict.update(newentry)

with open("/scratch1/jslim/nt.pickle", 'wb') as handle:
    pickle.dump(ntdict, handle, protocol=pickle.HIGHEST_PROTOCOL)
