# getMito
## Script to extract GenBank accession numbers of 12S rRNA gene sequences or mitochondrial sequences from a user-defined species list

From a user-provided list of genera/species/subspecies, this script extracts the corresponding GenBank accession numbers of their 12S rRNA sequences (reference file: <b>12S.list</b>) or mitochondrial sequences (reference file: </b>mitofish.hit.list</b>), if available. These accession numbers are prepared from downloaded MitoFish (Apr 2 2020 update) and NCBI data (Apr 12 2020 version). For data preparation pipeline, refer to </b>getMito.ipynb</b> or the <b>Preparing MitoFish data</b>, <b>Preparing NCBI data</b> and <b>Linking MitoFish data with NCBI data</b> sections below.

## Usage
There are two versions of this script:
- getMito.ipynb (python) - Run in Jupyter notebook interactively. Scroll down to the last cell in the notebook, click "Run", and type in three inputs sequentially in the white box below the cell: #1 input file (with extension; e.g. input.txt), #2 output prefix (e.g. OUT) and #2 reference database (12S.list or mitofish.hit.list)
- getMito.sh (shell) - Usage: getMito.sh <inputfile> <output_prefix> <12S.list or mitofish.hit.list>

Example:
<b>getMito.sh input.txt OUT mitofish.hit.list</b> will search the list of mitochondrial accession numbers and genes. Results for different taxonomic levels will be saved as <b>OUT</b>_genus.hits.txt, <b>OUT</b>_species.hits.txt and <b>OUT</b>_fulltaxonomy.hits.txt

## Reference files:
Reference files were prepared from downloaded <b>MitoFish (Apr 2 2020 update</b>) and <b>NCBI data (Apr 12 2020 version</b>). For data preparation pipeline, refer to <i>getMito.ipynb</i>, or the <i>Preparing MitoFish data</i>, <i>Preparing NCBI data</i> and <i>Linking MitoFish data with NCBI data</i> sections below:

A user can choose from two reference files:
- <b>12S.list</b> - List of NCBI acession numbers and gene description for 12S rRNA genes. Available at this GitHub repository.
- <b>mitofish.hit.list</b> - List of NCBI acession numbers and gene description for mitochondrial genes/genomes. Due to GitHub's file size limitation, this file (~516 MB) could not be uploaded here. Download from: https://drive.google.com/file/d/15KCkNB_EHN-dBG3bW3L6xnTgEUR5innm/view?usp=sharing
 
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

### !!! Input file warning !!!
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
### Output file redundancy
Note that some output files can be <b>redundant</b> to each other, depending on the taxonomic level. For example, if you performed a genus-level search, outputprefix_genus_hits.txt and outputprefix_species.hits.txt and outputprefix_fulltaxonomy.hits.txt will have the same information. If you performed a species-level search, outputprefix_species.hits.txt and outputprefix_fulltaxonomy.hits.txt will have the same information. 

## Preparing MitoFish data

MitoFish website: http://mitofish.aori.u-tokyo.ac.jp/download.html

### Download and process mitoannotator (complete mitogenome) records:

```
# Download and unzip file in a folder named 'mitoannotations'
mkdir mitoannotations
cd mitoannotations
wget http://mitofish.aori.u-tokyo.ac.jp/files/mitoannotations.zip
unzip mitoannotations.zip

# get accession numbers
ls *.txt | cut -d '_' -f1,2 >complete.accession

# get species names
ls *.txt | cut -d '_' -f3- | sed "s/.txt/#complete mitogenomes/g" >complete.species

# Make a list of accession number and species, separated by "#"
paste -d "#" complete.accession complete.species >complete.list

```
#### Download and process complete+partial mDNA sequence file: 

```
# Download and unzip sequence file in the same "mitoannotations" folder
wget http://mitofish.aori.u-tokyo.ac.jp/files/complete_partial_mitogenomes.zip
unzip complete_partial_mitogenomes.zip

# get accession numbers
grep ">" complete_partial_mitogenomes.fa | awk -F "|" '{print $2}' >mitofish.accession
```
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
### Get accession numbers
```
grep ">" nt | cut -d ' ' -f1 | tr -d ">"  >nt.accession 
```
### Get gene names
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

## Linking MitoFish data with NCBI data
This python script creates a dictionary from the nt.list file. The key is the NCBI accession number and the value is the gene description. This dictionary is then saved as a pickle named <b>nt.pickle</b>.

```
#!/usr/bin/python
import pickle
ntdict = {'Accession':'Gene description'}

with open("nt.list",'r') as f:
    for line in f:
        line = line.rstrip()
        entry = line.split("#")
        fullacc=entry[0].split(".")
        newentry={fullacc[0]:entry[1]} 
        ntdict.update(newentry)

with open("nt.pickle", 'wb') as handle:
    pickle.dump(ntdict, handle, protocol=pickle.HIGHEST_PROTOCOL)
 ```
This second python script loads nt.pickle, then matches MitoFish entries with keys (NCBI accession numbers) in the pickle. It takes ~24 minutes to match 616,999 MitoFish records to 57,377,397 NCBI GenBank records. <i>Resources used: 
cpupercent=101,cput=00:22:53,mem=34500088kb,ncpus=24,vmem=34845840kb,walltime=00:23:34</i>

```
#!/usr/bin/python

import pickle

import sys
import os.path
from os import path

with open("nt.pickle", 'rb') as handle:
    NCBI = pickle.load(handle)

outfile="mitofish.genes"
nohit=0
count=0
length=(len(NCBI))

if path.exists(outfile) :
    sys.exit("Error: Output file exists! Please rename output file and try again!")

output=open(outfile,'a')

print("==== Searching... ====")

with open("mitofish.accession",'r') as infile:
    for inline in infile:
        inline = inline.rstrip()
        count +=1
        if inline in NCBI:
            output.write("%s#%s\n" % (inline,NCBI[inline]))
        elif inline not in NCBI:
            output.write("%s#No hit found!\n" % inline)
            print("%s#No hit found!" % inline)
            nohit +=1
            
output.close()

print ("==== Run complete! ===")
print ("Total: %d accession numbers" % count)
print ("No hits for %d input accession numbers!" % nohit)
```
### Pick up "missing" accession numbers 

In NCBI fasta files, records with duplicate sequences will be concatenated in the header line, e.g.

```
>LN610233.1 Chiloglanis anoterus mitochondrial partial D-loop, specimen voucher 68321_34LN610234.1 Chiloglanis anoterus mitochondrial partial D-loop, specimen voucher 68330_55
```
These will not be picked up by the python script above. First, let's extract the accession numbers with no hits into an output file named <b>nohit.accession</b>.
```
grep "No hit" mitofish.genes | awk -F "#" '{print $1}' | sed "s/$/.[0-9]/g" >nohit.accession
```
We added some regular expression patterns to the accession numbers with no hits so that the grep search is more specific. The output file <b>nohit.accession</b> looks like this:

```
LN610210.[0-9]
LN610216.[0-9]
LN610224.[0-9]
LN610229.[0-9]
LN610230.[0-9]
LN610231.[0-9]
LN610232.[0-9]
LN610234.[0-9]
LN610235.[0-9]
```
We will also extract the hits from the python search for later use. Output file is <b>hit.list</b>:
```
grep -v "No hit" mitofish.genes >hit.list
```

Next, split up the reference file (<b>nt.genenames</b> generated in previous step) into smaller chunks of 1 million lines each. Each split file will have the prefix x followed by a number e.g. x00, x01

```
cd NCBI
split -d -l 1000000 nt.genenames
cd ..
```

For each accession number with no hit, search each chunk of nt.genenames for matches using all processors (-P 0). -n 1 specifies the number of argument to pass per command line. This takes ~39 hours to run for 144,308 accession numbers.

```
for id in $(cat nohit.accession)
do
string=`ls NCBI/x* | xargs -n 1 -P 0 grep $id`
echo "$id%$string" >>nohit.genes
done
```
Output file is <b>nohit.genes</b>. First, let's clean up the output file by removing non-specific matches and removing the regular expression patterns following the accession numbers:

```
grep "#" nohit.genes | sed "s/.\[0\-9\]//g" >nohit.genes.clean
```

Now, combine <b>hit.list</b> (accession numbers with exact matches with NCBI accession numbers) with <b>nohit.genes.clean</b> (accession numbers with duplicated sequences). The output file will be <b>mitofish.hit.list</b>:
```
cat hit.list nohit.genes.clean >mitofish.hit.list
```

 
