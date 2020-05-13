#!/usr/bin/python

import click
import sys
import os.path
from os import path

@click.command()
@click.option('-i','--input_file', required=True, type=str, help='Input query file (e.g. input.txt)')
@click.option('-o','--output_prefix', required=True, type=str, help='Output prefix (e.g. OUT)')

def getMito(input_file,output_prefix):
    """Script to fetch genus, species, or subspeices belonging to a specified list of taxa category (family,order,class,and phylum). The *.txt output can then be used for getMito.py"""

    filein=tuple(open(input_file,'r'))
    reference_file='eukaryota.tsv'
    i=0
    taxlist=["phylum","class","order","family","genus","species","subspecies"]

    # Throw an error message and exit if output file(s) already exist
    tsv=str(output_prefix+"_taxa.tsv")
    txt=str(output_prefix+"_taxa.txt")

    if path.exists(tsv) or path.exists(txt) :
        sys.exit("Error: Output file exists! Please rename output file and try again!")

    # This function looks up input taxa category and returns output taxonomic names

    def lookup(name,level,searchlevel):
        count=0
        output1=open(tsv,'a')
        output2=open(txt,'a')
        qcount=i+1

        with open(reference_file, 'r') as f:
            for rline in f.readlines():
                linelist=rline.rsplit("\t")

                if (name.casefold()==linelist[level].casefold()):
                    hit=linelist[searchlevel].rstrip("\n")

                    if (hit!=""):
                        output1.write("%s\t%s\t%s\t%s\n" % (name.capitalize(),taxlist[level],hit,taxlist[searchlevel]))
                        output2.write("%s\n" % hit)    
                        count +=1 
        output1.close()
        output2.close()
        print("Query #%d:%s\tQuery level:%s\tSearch level:%s\t# hits:%d" % (qcount,name.capitalize(),taxlist[level],taxlist[searchlevel],count))
        return;


    while (i < len(filein)):

        # Split input string into input taxa name, input taxonomic level, output taxonomic level
        line=str(filein[i]).rsplit("\t")
        intaxa=line[0]

        inlevel=0
        if(line[1].casefold()=="Phylum".casefold()):
            inlevel=0
        elif(line[1].casefold()=="Class".casefold()):
            inlevel=1
        elif(line[1].casefold()=="Order".casefold()):
            inlevel=2
        elif(line[1].casefold()=="Family".casefold()):
            inlevel=3

        outlevel=0  
        search=line[2].rsplit("\n")
        if(search[0].casefold()=="Genus".casefold()):
            outlevel=4
        elif(search[0].casefold()=="Species".casefold()):
            outlevel=5
        elif(search[0].casefold()=="Subspecies".casefold()):
            outlevel=6 

        lookup(name=intaxa,level=inlevel,searchlevel=outlevel)

        i += 1

if __name__ == '__main__':
    getMito()

