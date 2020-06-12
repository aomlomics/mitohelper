#!/usr/bin/python

import click
import sys
import os.path
from os import path
import pickle

@click.command()
@click.option('-i','--input_file', required=True, type=str, help='Input query file containing accession numbers')
@click.option('-t','--intype',required=True,type=str,help='Input file type: either getmito or plain')
@click.option('-r','--reference_file', required=True, type=str, help='Sequence reference file, e.g. 12S.pickle, COI.pickle or mitofish.pickle')
@click.option('-o','--output_file', required=True, type=str, help='Output file name (e.g. output.fasta)')

def getSeq(input_file,intype,reference_file,output_file):

    acc=tuple(open(input_file,'r'))

    # Throw an error message and exit if output file(s) already exist

    if path.exists(output_file):
        sys.exit("Error: Output file exists! Please rename output file and try again!")

    nohit=0
    count=0

    # This function does the sequence matching

    def matchseq(query):
        with open(reference_file, 'rb') as handle:
            seqpickle = pickle.load(handle)

        length=(len(seqpickle))

        output=open(output_file,'a')

        if query in seqpickle:
            print("%s:\tSequence match found!" % query)
            output.write(">%s\n%s\n" % (query,seqpickle[query]))

        elif query not in seqpickle:
            print("%s:\tNo hit found!" % query)

        output.close()

    if "mito" in intype:
        print("== Searching for sequences from getMito output ==")
        i = 0  
        seen=set()

        while (i < len(acc)):

            # Extract accession number from MitoFish output

            line=str(acc[i]).rsplit("\t")
            inquery=str(line[2])

            # Match each unique query
            if inquery not in seen:
                matchseq(query=inquery)
                seen.add(inquery)
            else:
                print("Duplicate warning: Accession %s has already been processed." % inquery)

            i += 1

    if "plain" in intype:
        print("== Searching for sequences from user's list ==")
        i = 0  
        seen=set()

        while (i < len(acc)):

            # Extract accession number from MitoFish output

            line=str(acc[i]).rsplit()
            inquery=str(line[0])
            # Match each unique query
            if inquery not in seen:
                matchseq(query=inquery)
                seen.add(inquery)
            else:
                print("Duplicate warning: Accession %s has already been processed." % inquery)

            i += 1


    print("== Search complete! ==")

if __name__ == '__main__':
    getSeq()
