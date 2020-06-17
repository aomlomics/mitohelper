#!/usr/bin/python

import click
import sys
import os.path
from os import path

@click.command()
@click.option('-i','--input_file', required=True, type=str, help='Input query file (e.g. input.txt)')
@click.option('-o','--output_prefix', required=True, type=str, help='Output prefix (e.g. OUT)')
@click.option('-r','--reference_file', required=True, type=str, help='Database file: either 12S.ref.tsv or mitofish.ref.tsv')

def getMito(input_file,output_prefix,reference_file):
    """Script to extract GenBank accession numbers of 12S rRNA gene sequences or mitochondrial sequences from a user-defined subspecies/species/genus list"""
    ref=tuple(open(input_file,'r'))
    full_path=str(output_prefix+"_subspecies.hits.tsv")
    species_path=str(output_prefix+"_species.hits.tsv")
    genus_path=str(output_prefix+"_genus.hits.tsv")

    # Throw an error message and exit if output file(s) already exist

    if path.exists(full_path) or path.exists(species_path) or path.exists(genus_path) :
        sys.exit("Error: Output file exists! Please rename output file and try again!")
    
    # This function performs matching at the specified level and writes results to the corresponding output file
    # Output files are tab-separated with the following columns:
    # Query, taxonomic level, GenBank accession number, gene description
    def matchme(query,level):
    	count=0
    	outpath=str(output_prefix+"_"+level+".hits.tsv")
    	output=open(outpath,'a')
    	with open(reference_file, 'r') as f:
        	for line in f.readlines():
            		if query in line:
                    		count += 1
                    		output.write("%s\t%s\t%s" % (query,level,line))
    	output.close()
    	print("Query:%s\tLevel:%s\t# Hits:%d" % (query,level,count))
    	return;


    # The while loop below goes through the input file line by line 
    i = 0
    seen=set()

    while (i < len(ref)):

        # Split string in query into genus,species, and subspecies (if present)
        taxa=str(ref[i]).rsplit()
        fulltaxa=str(ref[i]).rsplit("\n")
        fullquery=str(fulltaxa[0])
        gquery=str(taxa[0])

        # Check if species string exist in query
        if (len(taxa)>1):
            squery=str(taxa[0]+" "+taxa[1])

        qcount = i+1
        
        if (len(fullquery)<2 or len(squery)<2 or len(gquery)<2):
            print ("=== Searching user query #%d ===" % qcount)
            print("ERROR: Query: <%s> has name(s) that is/are too short! Skipping search..." % fullquery)            

        else:
            print ("=== Searching user query #%d ===" % qcount)

    # These if statements determine the level of matching (subspecies/species/genus) for each UNIQUE query 

            if (fullquery==gquery):
                if fullquery not in seen:
                    matchme(query=fullquery,level="genus")
                    seen.add(fullquery)
                else:
                    print("Duplicate warning: Genus %s has already been processed." % fullquery)

            elif (fullquery==squery):
                if fullquery not in seen:
                    matchme(query=fullquery,level="species")
                    seen.add(fullquery)
                else:
                    print("Duplicate query: Species %s has already been processed." % fullquery)
                if gquery not in seen:
                    matchme(query=gquery,level="genus")
                    seen.add(gquery)
                else:
                    print("Duplicate query: Genus %s has already been processed." % gquery)

            else:
                if fullquery not in seen:
                    matchme(query=fullquery,level="subspecies")
                    seen.add(fullquery)
                else:
                    print("Duplicate query: Species %s has already been processed." % fullquery)
                if squery not in seen:
                    matchme(query=squery,level="species")
                    seen.add(squery)
                else:
                    print("Duplicate query: Species %s has already been processed." % squery)
                if gquery not in seen:
                    matchme(query=gquery,level="genus")
                    seen.add(gquery)
                else:
                    print("Duplicate query: Genus %s has already been processed." % gquery)

        i += 1

    print ("==== Run complete! ===")

    # Check and report on the types of output files generated 

    if path.exists(genus_path): 
        print ("Accession numbers of genus hits and description saved in %s" % genus_path)
    else:
        print("No genus detected in input file.")

    if path.exists(species_path):
        print ("Accession numbers of species hits and description saved in %s" % species_path)
    else:
        print("No species detected in input file.")
    
    
    if path.exists(full_path):
    	print ("Accession numbers of subspecies hits and description saved in %s" % full_path)
    else:
    	print("No subspecies detected in input file.")

if __name__ == '__main__':
    getMito()

