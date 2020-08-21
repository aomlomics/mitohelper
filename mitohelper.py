#!/usr/bin/python

import click
import sys
import subprocess
import os
from os import path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

@click.group()

def mitohelper():
	pass

@mitohelper.command()
@click.option('-i','--input_file', required=True, type=str, help='Input query file (e.g. input.txt)')
@click.option('-o','--output_prefix', required=True, type=str, help='Output prefix (e.g. OUT)')
@click.option('-d','--database_file', required=True, type=str, help='Database file (e.g. mitofish.all.Jul2020.tsv')
@click.option('-l','--tax_level',type=click.Choice(["1","2","3","4","5","6","7"]), help='The taxonomic level of the search (e.g 7 for species, 6 for genus etc)')
@click.option('--fasta/--no-fasta', default=False, help='Generate FASTA file output containing sequences of all matching hits (default=FALSE)')

def getrecord(input_file,output_prefix,database_file,tax_level,fasta):
	
	"""Retrieve fish mitochondrial records from taxa list"""

	# Throw various error messages and exit if tax_level is not set or output file(s) already exist

	if not tax_level:
		sys.exit("Error: Taxonomic level of the search (-l option) is not specified!")

	ref=tuple(open(input_file,'r'))
	full_path=str(output_prefix+"_L"+tax_level+"_hits.tsv")

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
						if levelname.lower() not in seen:
							seen.add(levelname.lower())	
							matchme(query=levelname)
							break
						if levelname.lower() in seen:
							print("DUPLICATE WARNING: Query has already been processed!")
							break
				i += 1
	f.close()
	output.close()
	print ("==== Run complete! ===")
	print ("Accession numbers of subspecies hits and description saved in %s" % full_path)

	if fasta:
		print ("FASTA-formatted sequences saved in %s" % fasta_path)



@mitohelper.command()
@click.option('-i','--input_file', required=True, type=str, help='Input file: either blast output file or FASTA file')
@click.option('-o','--output_prefix', required=True, type=str, help='Output prefix (e.g. OUT)')
@click.option('-r','--reference_sequence', required=False, type=str, help='FASTA file of a single reference sequence for blastn searches. Required for --blast option.')
@click.option('--blast/--no-blast', default=False, help='Perform local blastn-short searches to extract alignment positions (default=FALSE)')

def getalignment(input_file,output_prefix,reference_sequence,blast):
	
	"""Pairwise align input sequences against a reference"""
	
	pdf_out=(output_prefix+".alnpositions.pdf")
	tsv_out=(output_prefix+".alnpositions.tsv")

	# Throw an error message and exit if output file(s) exist(s)

	if path.exists(pdf_out or tsv_out):
		sys.exit("Error: Output PDF and/or TSV file(s) exist(s)! Please rename/delete output file(s) and try again!")

	# This parse_blast function extracts alignment position(s) with the highest bit score from the blastn-short output  

	def parse_blast(results):
		hits=tuple(open(results,'r'))
		outfile=open(tsv_out,'a')
		outfile.write("Accession\tStart\tEnd\n")
		i = 0
		seen=set()

		query=None
		startmin=None
		endmax=None
		lastscore=None

		while (i < len(hits)):
			line=str(hits[i])
				
			if line.startswith ('#'):
				i += 1

			if not line.startswith ('#'):
				full=line.rsplit("\t")
				acc=str(full[0])
				sstart=int(full[8])
				send=int(full[9])
				score=float(full[11])
				
				if (acc not in seen):

					if (i>0):
						if (query is not None):
							outfile.write("%s\t%s\t%s\n" % (query,startmin,endmax))
					if (i>=0):
						seen.add(acc)	
						query=acc
						startmin=int(sstart)
						endmax=int(send)
						lastscore=float(score)
						
				if (acc==query and score==lastscore):
					startmin=min(startmin,sstart)
					endmax=max(endmax,send)
 

				i += 1
				

			if (i==(len(hits)-1)):
				outfile.write("%s\t%s\t%s\n" % (query,startmin,endmax))

		outfile.close()


	if blast:
		blast_out=(output_prefix+".blastn.txt")
		blast_query=(output_prefix+".blastquery.fasta")
		if path.exists(blast_out):
			sys.exit("Error: Output blastn output file exists! Please rename/delete output file and try again!")
		if reference_sequence is None:
			sys.exit("Error: Reference sequence for blast search (-r option) is not specified!")
		
		# Merge reference sequence and input sequences for blast search
		# Reference sequence will always be the first sequence in output

		filenames = [reference_sequence, input_file]
		with open(blast_query, 'w') as merge:
    			for fname in filenames:
        			with open(fname) as infasta:
            				merge.write(infasta.read())

		blastn=subprocess.Popen(['blastn', '-task', 'blastn-short', '-query', blast_query, '-subject', reference_sequence, '-outfmt', '7', '-out', blast_out])
		blastn.communicate()
		parse_blast(blast_out)
		os.remove(blast_query)

	if not blast:
		parse_blast(input_file)

	positions=pd.read_table(tsv_out)
	positions=pd.melt(positions,"Accession",var_name="PositionType")
	positions.columns=['Accession','PositionType','Position']

	start = positions[positions["PositionType"] == "Start"]
	end = positions[positions["PositionType"] == "End"]
	
	sns.set(style="white")

	posplot=sns.pointplot(x="Position", y="Accession", hue="Accession", markers="", data=positions)
	posplot.legend_.remove()
	plt.title("Sequence alignment(s) relative to reference", size=14)
	plt.grid(linestyle=":")

	for xmin,ymin in enumerate(start['Position']):
  		if(ymin==1):
    			plt.text(-30,xmin,ymin,fontsize=8,bbox=dict(facecolor='lightgrey', alpha=0.5))
  		if(ymin>1):
    			plt.text(ymin-70,xmin,ymin,fontsize=8,bbox=dict(facecolor='lightgrey', alpha=0.5))

	for xmax,ymax in enumerate(end['Position']):
    		plt.text(ymax+30,xmax,ymax,fontsize=8,bbox=dict(facecolor='lightgrey', alpha=0.5))
	
	plt.savefig(pdf_out,bbox_inches='tight')

	print ("==== Run complete! ===")

	if blast:
		print ("blastn output saved in %s" % blast_out)

	print ("Table of alignment positions saved in %s" % tsv_out)
	print ("Plot of alignment positions saved in %s" % pdf_out)

if __name__ == '__main__':
	mitohelper()
