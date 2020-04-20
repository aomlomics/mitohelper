# get12S - Script to extract GenBank accession numbers of 12S rRNA gene sequences from a user-defined species list


From a user-provided list of genera/species/subspecies, this script extracts the corresponding GenBank accession numbers of their 12S rRNA sequences, if available. The 12S rRNA gene accession numbers (<b>12S.list</b>) are prepared from downloaded NCBI data (see section below).

There are two versions of this script:
- get12S.ipynb (python) - Run in Jupyter notebook
- get12S.sh (shell) - Usage: get12S.sh input_file output_prefix 

## Input file:
Plain text file, with each line containing a genera, species, or subspecies. Test data are in the <b>fishdata</b> subfolder. <br>
e.g.
```
Argyropelecus aculeatus
Argyropelecus affinis
Argyropelecus gigas
Argyropelecus hemigymnus
Argyropelecus olfersii
Argyropelecus sladeni
Aristostomias xenostoma
Astronesthes atlanticus
Astronesthes gemmifer
```

## !!! Input file warning !!!
For best results, do not add different taxa hierarchies in the same input file. 
e.g.
```
Argyropelecus aculeatus
Argyropelecus affinis
Argyropelecus gigas
Astronesthes
Aristrostomias
```
Have a separate file for genus names only (if you only have genus information), species names (if you have species information), and subspecies names (if you have subspecies information). Else, the output files will contain a mix of genus, species and subspecies hits.

## Output files:
3 output files will be generated 
- <b>outputprefix</b>_genus.hits.txt
- <b>outputprefix</b>_species.hits.txt 
- <b>outputprefix</b>_fulltaxonomy.hits.txt
  
Output file is separated by "#" in the format: GenBank_Accession#Gene_description
e.g.
```
NCBIAF092181.1#Alepisaurus ferox 12S ribosomal RNA gene, mitochondrial gene for mitochondrial RNA, partial sequence
LC021097.1#Alepisaurus ferox mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: CBM:ZF:10875
LC091793.1#Alepisaurus ferox mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: HUMZ:221156
LC091794.1#Alepisaurus ferox mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: UW:117706
LC091795.1#Alepisaurus ferox mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: UW:113571
AF092200.1#Anoplogaster cornuta 12S ribosomal RNA gene, mitochondrial gene for mitochondrial RNA, partial sequence
```

Note that some output files can be <b>redundant</b> to each other, depending on the taxonomic level. For example, if you performed a genus-level search, outputprefix_genus_hits.txt and outputprefix_species.hits.txt and outputprefix_fulltaxonomy.hits.txt will have the same information. If you performed a species-level search, outputprefix_species.hits.txt and outputprefix_fulltaxonomy.hits.txt will have the same information. 

## Preparing NCBI data (done in Unix environment)

NCBI blast databases ftp site: https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/

### Download and unzip NCBI sequence file in the "NCBI" subfolder
```
cd NCBI
wget https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz
wget https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz.md5
md5sum -c nt.gz.md5 >md5sum.log
unzip nt.gz
```
### get accession numbers
```
grep ">" nt | cut -d ' ' -f1 | tr -d ">"  >nt.accession 
```
### get gene names
```
grep ">" nt | cut -d ' ' -f2- >nt.genenames 
```
### Make a list of accession number and species, separated by "#"
```
paste -d "#" nt.accession nt.genenames >nt.list
```
### Extract (grep) 12S genes from NCBI records and create the 12S.list reference 
```
grep -e "12S ribosomal" -e "12S rRNA" nt.list >12S.list
```
