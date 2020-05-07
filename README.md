# getMito
#### Scripts to extract GenBank accession numbers of 12S rRNA gene sequences or mitochondrial sequences from a user-defined subspecies/species/genus list

- From a user-provided list of genera/species/subspecies, this script extracts the corresponding GenBank accession numbers of their 12S rRNA sequences (reference file: <b>12S.ref.tsv</b>) or mitochondrial sequences (reference file: </b>mitofish.ref.tsv</b>), if available. - These accession numbers are prepared from downloaded MitoFish (Apr 2 2020 update) and NCBI data (Apr 12 2020 version). 
- For data preparation pipeline, refer to </b>getMito.ipynb</b> or the <i>Preparing MitoFish data</i>, <i>Preparing NCBI data</i> and <i>Linking MitoFish data with NCBI data</i> sections below.

## Usage
There are two versions of this script:
1. <b>getMito.ipynb</b> (python) - Run in Jupyter notebook interactively. Scroll down to the last cell in the notebook, click "Run", and type in three inputs sequentially in the white box below the cell: 
 - Input file (with extension; e.g. input.txt)
 - Output prefix (e.g. OUT)
 - Reference database (12S.ref.tsv or mitofish.ref.tsv)
2. <b>getMito.sh</b> (shell) - Usage: getMito.sh <inputfile> <output_prefix> <12S.list or mitofish.hit.list>. 
 <br>This is almost the same as the python script, with slight differences in the format of the output files and log (see <i>output files</i> and <i>output log</i> section below).


## Reference files:
Reference files were prepared from downloaded <b>MitoFish (Apr 2 2020 update</b>) and <b>NCBI data (Apr 12 2020 version</b>). For data preparation pipeline, refer to <i>getMito.ipynb</i>, or the <i>Preparing MitoFish data</i>, <i>Preparing NCBI data</i> and <i>Linking MitoFish data with NCBI data</i> sections below:

A user can choose from two reference files:
1. <b>12S.ref.tsv</b> - Tab-separated list of NCBI acession numbers and gene description for 12S rRNA genes. Available here.
2. <b>mitofish.ref.tsv</b> - Tab-separated list of NCBI acession numbers and gene description for mitochondrial genes/genomes. Due to GitHub's file size limitation, this file (~502 MB) could not be uploaded here. Download from: https://drive.google.com/file/d/176hJjezjGTdGL3wYu4yM7nPmUV57Oiav/view?usp=sharing
 
## Input file:
Plain text file, with each line containing a genera, species, or subspecies. Test data are in the <b>fishdata</b> subfolder. <br>
e.g.
```
Histioteuthis celetaria celetaria
Histioteuthis corona corona
Stomias boa boa
Lampadena urophaos atlantica
```

## Output files:
One to two output files will be generated, depending on the taxonomic level of your query.
<br>For example, if there are no subspecies in your query file, no subspecies hits file will be generated.
<br>If none of the subspecies in your query file returns a hit, a blank subspecies hits file will be generated.
- <<b>outputprefix</b>>_genus.hits.tsv
- <<b>outputprefix</b>>_species.hits.tsv 
- <<b>outputprefix</b>>_subspecies.hits.tsv
  
Output file is tab-separated with the following fields: 
- <b>Query, taxonomic level, GenBank accession number, gene description</b>

<br>Example output file <<i>OUT_species.hits.tsv</i>>:
```
Stomias boa     species KX929921.1      Stomias boa voucher ZMUC P2014774 12S ribosomal RNA gene, partial sequence; mitochondrial
Stomias boa     species LC458106.1      Stomias boa mitochondrial gene for 12S rRNA, partial sequence
Lampadena urophaos      species LC026535.1      Lampadena urophaos urophaos mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: HUMZ:220996
Lampadena urophaos      species LC026536.1      Lampadena urophaos urophaos mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: HUMZ:221119
Lampadena urophaos      species LC146002.1      Lampadena urophaos mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: CBM:ZF:14569
Alepisaurus ferox       species AF092181.1      Alepisaurus ferox 12S ribosomal RNA gene, mitochondrial gene for mitochondrial RNA, partial sequence
Alepisaurus ferox       species LC021097.1      Alepisaurus ferox mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: CBM:ZF:10875
Alepisaurus ferox       species LC091793.1      Alepisaurus ferox mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: HUMZ:221156
Alepisaurus ferox       species LC091794.1      Alepisaurus ferox mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: UW:117706
Alepisaurus ferox       species LC091795.1      Alepisaurus ferox mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: UW:113571
Anoplogaster cornuta    species AF092200.1      Anoplogaster cornuta 12S ribosomal RNA gene, mitochondrial gene for mitochondrial RNA, partial sequence
Anoplogaster cornuta    species LC026573.1      Anoplogaster cornuta mitochondrial gene for 12S rRNA, partial sequence
```
### ! Output file differences between python and shell versions !
- The python version always outputs the correct query in the first field. 
- In the shell version, the query is "back calculated" from the output file, so if the hit GenBank record contains a duplicate sequence from another taxon, the first taxon will always be reported as the query.

<br>In the example below, GenBank record JN311785 is matched to two species Chauliodus sloani and Stomias sp. If the user's query is "Stomias", the python version will output the correct query in the first column:
```
Stomias       genus   JN312424        Chauliodus sloani voucher BW-A10860 cytochrome oxidase subunit 1 (COI) gene, partial cds; mitochondrialJN312424.1 Stomias sp. FOAN072-11 voucher BW-A10865 cytochrome oxidase subunit 1 (COI) gene, partial cds; mitochondrial
```
The shell version will output the query as Chauliodus instead of Stomias, because it is the first taxon represented in the GenBank record:
```
Chauliodus    genus   JN311785        Chauliodus sloani voucher BW-A10860 cytochrome oxidase subunit 1 (COI) gene, partial cds; mitochondrialJN312424.1 Stomias sp. FOAN072-11 voucher BW-A10865 cytochrome oxidase subunit 1 (COI) gene, partial cds; mitochondrial
```

## Output log:
While running, the script will also print out your query, and the number of hits for each matching taxonomic level to the screen. 

### ! Output log differences between python and shell versions !
- In the python version, duplicated query/queries, if present, will be marked as "Duplicate query:"
- In the shell version, duplicated query/queries will be counted as usual and not be marked as "Duplicate query". However, the output file will still be deduplicated.

<br>Python screen output:
```
=== Searching user query #1 ===
Query:Histioteuthis celetaria celetaria	Level:subspecies	# Hits:0
Query:Histioteuthis celetaria	Level:species	# Hits:0
Query:Histioteuthis	Level:genus	# Hits:1
=== Searching user query #2 ===
Query:Histioteuthis corona corona	Level:subspecies	# Hits:0
Query:Histioteuthis corona	Level:species	# Hits:0
Duplicate query: Genus Histioteuthis has already been processed.
=== Searching user query #3 ===
Query:Stomias boa boa	Level:subspecies	# Hits:0
Query:Stomias boa	Level:species	# Hits:2
Query:Stomias	Level:genus	# Hits:11
=== Searching user query #4 ===
Query:Lampadena urophaos atlantica	Level:subspecies	# Hits:0
Query:Lampadena urophaos	Level:species	# Hits:3
Query:Lampadena	Level:genus	# Hits:5
 ```
<br>Shell screen output:
```
=== Searching query #1====
Query:Histioteuthis celetaria celetaria Level:subspecies        # Hits: 0
Query:Histioteuthis celetaria   Level:species   # Hits: 0
Query:Histioteuthis     Level:genus     # Hits: 1
=== Searching query #2====
Query:Histioteuthis corona corona       Level:subspecies        # Hits: 0
Query:Histioteuthis corona      Level:species   # Hits: 0
Query:Histioteuthis     Level:genus     # Hits: 1
=== Searching query #3====
Query:Stomias boa boa   Level:subspecies        # Hits: 0
Query:Stomias boa       Level:species   # Hits: 2
Query:Stomias   Level:genus     # Hits: 11
=== Searching query #4====
Query:Lampadena urophaos atlantica      Level:subspecies        # Hits: 0
Query:Lampadena urophaos        Level:species   # Hits: 3
Query:Lampadena Level:genus     # Hits: 5
```

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

# Make a tab-separated list of accession number and species
paste -d "\t" complete.accession complete.species >complete.list
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
### Make a tab-separated list of accession number and species
```
paste -d "\t" nt.accession nt.genenames >nt.list
cd ..
```
### Extract (grep) 12S genes from NCBI records and create the 12S.list reference 
```
grep -e "12S ribosomal" -e "12S rRNA" nt.list >12S.ref.tsv
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
        entry = line.split("\t")
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
            output.write("%s\t%s\n" % (inline,NCBI[inline]))
        elif inline not in NCBI:
            output.write("%s\tNo hit found!\n" % inline)
            print("%s\tNo hit found!" % inline)
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
grep -P '\t' nohit.genes | sed "s/.\[0\-9\]//g" >nohit.genes.clean
```

Now, combine <b>hit.list</b> (accession numbers with exact matches with NCBI accession numbers) with <b>nohit.genes.clean</b> (accession numbers with duplicated sequences). The output file will be <b>mitofish.hit.list</b>:
```
cat hit.list nohit.genes.clean >mitofish.hit.list
```

 
