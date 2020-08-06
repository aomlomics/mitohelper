#!/usr/bin/python

import click
import sys
from os import path

@click.command()
@click.option('-i','--input_file', required=True, type=str, help='Input query file (e.g. input.txt)')
@click.option('-o','--output_prefix', required=True, type=str, help='Output prefix (e.g. OUT)')
@click.option('-d','--database_file', required=True, type=str, help='Database file (e.g. mitofish.all.Jul2020.tsv')
@click.option('-l','--tax_level',type=click.Choice(["1","2","3","4","5","6","7"]), help='The taxonomic level of the search (e.g 7 for species, 6 for genus etc)')
@click.option('--fasta/--no-fasta', default=False, help='Generate FASTA file output containing sequences of all matching hits (default=FALSE)')

def getMito(input_file,output_prefix,database_file,tax_level,fasta):
	
	"""Script to extract mitochondrial sequence records from a user-provided list of fish taxonomic names"""
	ref=tuple(open(input_file,'r'))
	full_path=str(output_prefix+"_L"+tax_level+"_hits.tsv")

	# Throw an error message and exit if output file(s) already exist
	if path.exists(full_path):
		sys.exit("Error: Output TSV file exists! Please rename output TSV file and try again!")

	if fasta:
		fasta_path=(output_prefix+"_L"+tax_level+".fasta")
		if path.exists(fasta_path):
			sys.exit("Error: Output FASTA file exists! Please rename output FASTA file and try again!")
		fasta=open(fasta_path,'a')
		
	output=open(full_path,'a')
	output.write("Query\tAccession\tGene definition\ttxid\tSuperkingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\tSequence\n")

	# This matchme function performs matching and writes results to the output file
	def matchme(query):
		count=0

		with open(database_file, 'r') as db:
			for line in db.readlines():
				if query.casefold() in line.casefold():
					count += 1
					output.write("%s\t%s" % (query,line))
					if fasta:
						fields=line.rsplit("\t")
						acc=str(fields[0])
						seq=str(fields[10])
						fasta.write(">%s\n%s" % (acc,seq))

		print("Search string:%s\tTaxonomic level:L%s\tHits:%d" % (query,tax_level,count))
		return;


	column=int(tax_level)+2

	i = 0
	seen=set()

	while (i < len(ref)):
		# Process and count each query
		fulltaxa=str(ref[i]).rsplit("\n")
		fullquery=str(fulltaxa[0])
		qcount = i+1
        
		# Produce error if the query is <2 characters
		if (len(fullquery)<2):
			print ("=== Searching query #%d: <%s> ===" % (qcount,fullquery))
			print("ERROR: Query is too short (<2 characters)! Skipping search...")            
			i += 1

		else:
			print ("=== Searching query #%d: <%s> ===" % (qcount,fullquery))
			
			with open(database_file, 'r') as f:
				for line in f.readlines():
					if fullquery.casefold() in line.casefold():
						taxa=line.rsplit("\t")
						levelname=str(taxa[column])

						# Check for query duplicates at the specified taxonomic level, skip search if query is duplicated						
						if levelname not in seen:
							seen.add(levelname)	
							matchme(query=levelname)
							break
						else:
							print("DUPLICATE WARNING: Query has already been processed!")
							break
				i += 1
	f.close()
	output.close()
	print ("==== Run complete! ===")
	print ("Accession numbers of subspecies hits and description saved in %s" % full_path)

	if fasta:
		print ("FASTA-formatted sequences saved in %s" % fasta_path)

if __name__ == '__main__':
	getMito()

