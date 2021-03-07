#!/usr/bin/env python

import click
import sys
import subprocess
import os
from os import path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd

@click.group()

def mitohelper():
	pass

@mitohelper.command()
@click.option('-i','--input_file', required=True, type=str, help='Input query file (e.g. input.txt)')
@click.option('-o','--output_prefix', required=True, type=str, help='Output prefix (e.g. OUT)')
@click.option('-d','--database_file', required=True, type=str, help='Database file (e.g. mitofish.all.Jan2021.tsv)')
@click.option('-l','--tax_level',type=click.Choice(["1","2","3","4","5","6","7"]), help='The taxonomic level of the search (e.g 7 for species, 6 for genus etc)')
@click.option('--fasta/--no-fasta', default=False, help='Generate FASTA file output containing sequences of all matching hits (default=FALSE)')
@click.option('--taxout/--no-tax', default=False, help='Generate taxonomy file output for all matching hits (default=FALSE)')

def getrecord(input_file,output_prefix,database_file,tax_level,fasta,taxout):
	
	"""Retrieve fish mitochondrial records from taxa list"""

	# Throw various error messages and exit if tax_level is not set or output file(s) already exist

	if not tax_level:
		sys.exit("Error: Taxonomic level of the search (-l option) is not specified!")

	ref=tuple(open(input_file,'r'))
	full_path=str(output_prefix+"_L"+tax_level+"_hits.tsv")

	if path.exists(full_path):
		sys.exit("Error: Output TSV file exists! Please rename output TSV file and try again!")

	# Write header line in output file
	output=open(full_path,'a')
	output.write("Query\tAccession\tGene definition\ttaxid\tSuperkingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\tSequence\tOrderID\tFamilyID\n")

	if fasta:
		fasta_path=(output_prefix+"_L"+tax_level+".fasta")
		if path.exists(fasta_path):
			sys.exit("Error: Output FASTA file exists! Please rename output FASTA file and try again!")
		fasta=open(fasta_path,'a')

	if taxout:
		tax_path=(output_prefix+"_L"+tax_level+".taxonomy.tsv")
		if path.exists(tax_path):
			sys.exit("Error: Output taxonomy file exists! Please rename output taxonomy file and try again!")
		taxfile=open(tax_path,'a')
		taxfile.write("Feature ID\tTaxon\n")

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
						fasta.write(">%s\n%s\n" % (acc,seq))
				
					if taxout:
						fields=line.rsplit("\t")
						acc=str(fields[0])
						domain=str(fields[3])
						phylum=str(fields[4])
						tclass=str(fields[5])
						order=str(fields[6])
						family=str(fields[7])
						genus=str(fields[8])
						species=str(fields[9])

						taxfile.write("%s\td__%s; p__%s; c__%s; o__%s; f__%s; g__%s; s__%s\n" % (acc,domain,phylum,tclass,order,family,genus,species))

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

	if taxout:
		print ("Output taxonomy file saved in %s" % tax_path)



@mitohelper.command()
@click.option('-i','--input_file', required=True, type=str, help='Input file: either blastn output file or FASTA file')
@click.option('-o','--output_prefix', required=True, type=str, help='Output prefix (e.g. OUT)')
@click.option('-r','--reference_sequence', required=False, type=str, help='FASTA file of a single reference sequence for blastn searches. Required for --blast option.')
@click.option('--blastn-task', type=click.Choice(['blastn','blastn-short','megablast','dc-megablast','none']), required=True, default='none', help='Choice of blastn task for local similarity searches used to extract alignment positions [default:blastn-short]')

def getalignment(input_file,output_prefix,reference_sequence,blastn_task):
	
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
		outfile.write("Accession\tStart\tEnd\tBit_Score\n")
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
							outfile.write("%s\t%d\t%d\t%d\n" % (query,startmin,endmax,lastscore))
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
				outfile.write("%s\t%d\t%d\t%d\n" % (query,startmin,endmax,lastscore))

		outfile.close()


	if (blastn_task!='none'):
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

		blastn=subprocess.Popen(['blastn', '-task', blastn_task, '-query', blast_query, '-subject', reference_sequence, '-outfmt', '7', '-out', blast_out])
		blastn.communicate()
		parse_blast(blast_out)
		os.remove(blast_query)

	if (blastn_task=='none'):
		parse_blast(input_file)

	positions=pd.read_table(tsv_out)
	positions=pd.melt(positions,['Accession','Bit_Score'],var_name='PositionType')
	positions.columns=['Accession','Bit_Score','PositionType','Position']

	start = positions[positions["PositionType"] == "Start"]
	end = positions[positions["PositionType"] == "End"]
	vmax = float(max(positions['Bit_Score']))
        
	if (vmax<200):
		vmax=500

	# Place bit scores into categories
	cut_cat=['<40','40-50','50-80','80-200','>=200']
	cut_bins =[0, 40, 50, 80, 200, vmax]
	cpalette ={0: 'k', 1: 'b', 2: 'lime', 3: 'm', 4: 'r'}

	positions['Score Category'] = pd.cut(positions['Bit_Score'], bins=cut_bins, labels = cut_cat)
	ncat=positions['Score Category'].nunique()
	positions['Bit Score Range'] = positions['Score Category'].cat.codes
	
	sns.set(style="white")

	posplot=sns.pointplot(x='Position', y='Accession', hue='Bit Score Range', palette=cpalette, join=False, markers="", data=positions)

	plt.title("Sequence alignment(s) relative to reference", size=14)
	plt.grid(linestyle=":")

	# Plot alignment positions on graph
	for xmin,ymin in enumerate(start['Position']):
  		if(ymin==1):
    			plt.text(-30,xmin,ymin,fontsize=8,bbox=dict(facecolor='lightgrey', alpha=0.5))
  		if(ymin>1):
    			plt.text(ymin-70,xmin,ymin,fontsize=8,bbox=dict(facecolor='lightgrey', alpha=0.5))

	for xmax,ymax in enumerate(end['Position']):
    		plt.text(ymax+30,xmax,ymax,fontsize=8,bbox=dict(facecolor='lightgrey', alpha=0.5))

	# Make customized legend
	red = mpatches.Patch(color='red')
	magenta = mpatches.Patch(color='m')
	lime = mpatches.Patch(color='lime')
	blue = mpatches.Patch(color='b')
	black = mpatches.Patch(color='k')
	plt.legend((red, magenta, lime, blue, black), ('>=200', '80-200', '50-80', '40-50', '<40'), loc='upper right', bbox_to_anchor=(1.4,1), title='Bit Scores')
	
	plt.savefig(pdf_out,bbox_inches='tight')

	print ("==== Run complete! ===")

	if (blastn_task!='none'):
		print ("blastn output saved in %s" % blast_out)

	print ("Table of alignment positions saved in %s" % tsv_out)
	print ("Plot of alignment positions saved in %s" % pdf_out)

if __name__ == '__main__':
	mitohelper()
