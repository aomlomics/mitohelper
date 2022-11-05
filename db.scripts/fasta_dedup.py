#!/usr/bin/env python

import os, glob
from os import path
import re

seen=set()
month=str("Nov2022")

with open("mitofish.12S."+month+".fasta", 'r') as fasta:
	outfile=str("mitofish.12S.Nov2022_NR.fasta")
	output=open(outfile,'w')
	for line in fasta.readlines():
		if re.search(">",line):
			header=line.rsplit("\n")
			seqheader=header[0]
			count=1

			if seqheader in seen:
				output.write(seqheader+"_"+str(count))	
				output.write("\n")
				count=count+1
	
			if seqheader not in seen:
				seen.add(seqheader)
				output.write(seqheader)
				output.write("\n")
		else:
			seq=line.rsplit("\n")
			output.write(seq[0])
			output.write("\n")
	fasta.close()
	output.close()
