#!/usr/bin/python
import pickle
seqdict = {'Accession':'Sequence'}

with open("mitofish.seqref.tsv",'r') as f:
    for line in f:
        line = line.rstrip()
        entry = line.split("\t")
        newentry={entry[0]:entry[1]} 
        seqdict.update(newentry)

with open("mitofish.pickle", 'wb') as handle:
    pickle.dump(seqdict, handle, protocol=pickle.HIGHEST_PROTOCOL)
