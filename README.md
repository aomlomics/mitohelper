# mitohelper

<b>mitohelper</b> is a repository built to facilitate experimental design, alignment visualization, and reference sequence analysis in fish eDNA studies. It is useful for researchers who are interested in:
- finding out whether mitochondrial reference sequences exist for specific fish species/taxonomy (```getrecord``` command in ```mitohelper.py```)
- finding out which specific region of a mitochondrial gene has been sequenced (by aligning with a reference sequence) (```getalignment``` command in ```mitohelper.py```)
- downloading pre-formatted QIIME-compatible ribosomal RNA (12S or 12S+16S+18S) sequence and taxonomy databases for downstream analysis (available in the ```QIIME-compatible``` folder) 
- knowing more about our data processing pipeline and mitohelper algorithm (visit the [DevWiki](https://github.com/shenjean/mitohelper/wiki/) for all the nitty gritty details!)

### Dependencies

- Tested on python 3.6.10
- For local blastn searches, NCBI [BLAST+ executables](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) (specifically `blastn`) must be installed and in the system path

```
Required python modules
- click (v7.1.2)
- matplotlib (v3.3.0)
- pandas (v0.25.3)
- seaborn (v0.10.1)
```

### Usage

```
Usage: mitohelper.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  getalignment  Pairwise align input sequences against a reference
  getrecord     Retrieve fish mitochondrial records from taxa list
```

### getrecord

```
Usage: mitohelper.py getrecord [OPTIONS]

  Retrieve fish mitochondrial records from taxa list

Options:
  -i, --input_file TEXT           Input query file (e.g. input.txt)
                                  [required]

  -o, --output_prefix TEXT        Output prefix (e.g. OUT)  [required]
  -d, --database_file TEXT        Database file (e.g. mitofish.all.Jul2020.tsv
                                  [required]

  -l, --tax_level [1|2|3|4|5|6|7]
                                  The taxonomic level of the search (e.g 7 for
                                  species, 6 for genus etc)

  --fasta / --no-fasta            Generate FASTA file output containing
                                  sequences of all matching hits
                                  (default=FALSE)

  --help                          Show this message and exit.
```

> Reference database files:
> - [mitofish.all.Aug2020.tsv](https://drive.google.com/uc?export=download&id=1VKVOpi3g13fm2g6s0-OedKHpNQf4dDNy) (640,002 records; Aug 2020 update)
> - [mitofish.12S.Aug2020.tsv](https://drive.google.com/uc?export=download&id=1VCoWikJHsHJIrQdb5IZfNIoqtMjgC3Td) (34,573 records)
> - [mitofish.COI.Aug2020.tsv](https://drive.google.com/uc?export=download&id=1VQuOkz8wGEli0C9uIChpJ9pDydcOSvBA) (199,311 records)

Input file example: 

```
Abraliopsis pfefferi
Ahliesaurus berryi
Alepisaurus FEROX
anotopterus pharao
```

Screen output example:

```
=== Searching query #1: <Abraliopsis pfefferi> ===
=== Searching query #2: <Ahliesaurus berryi> ===
Search string:Notosudidae       Taxonomic level:L5      Hits:55
=== Searching query #3: <Alepisaurus FEROX> ===
Search string:Alepisauridae     Taxonomic level:L5      Hits:79
=== Searching query #4: <anotopterus pharao> ===
DUPLICATE WARNING: Query has already been processed!
```

Output file example (e.g. OUT_L5_hits.tsv):

```
Query   Accession       Gene definition txid    Superkingdom    Phylum  Class   Order   Family  Genus   Species Sequence
Notosudidae     AP004201        Scopelosaurus hoedti mitochondrial DNA, almost complete genome  172128  Eukaryota       Chordata        Actinopteri     Au
lopiformes      Notosudidae     Scopelosaurus   Scopelosaurus hoedti    GCTAACGTAGTTTACTAAAAATATGACTCTGAAGAAGTTAAGACAGACCCTGAGAAGGCCTCGTAAGCACAAAAGCTTGGTC
CTGGCTTTACTGTCATCTCAAACCGAGCTTACACATGCAAGTCTCCGCACCCCTGTGAGGATGCCCTCCACCCTCCTTTCCGGAAACGAGGAGCCGGTATCAGGCACGCCTATCAAGGCAGCCCAAAACACCTTGCTCAGCCACACCCCCAAGG
GATTTCAGCAGTGATAGACATTAAGCAATAAGTGAAAACTTGACTTAGTTAAGGTTTAACAGGGCCGGTCAACCTCGTGCCAGCCGCCGCGGT
```

### getalignment

```
Usage: mitohelper.py getalignment [OPTIONS]

  Pairwise align input sequences against a reference

Options:
  -i, --input_file TEXT          Input file: either blast output file or FASTA
                                 file  [required]

  -o, --output_prefix TEXT       Output prefix (e.g. OUT)  [required]
  -r, --reference_sequence TEXT  FASTA file of a single reference sequence for
                                 blastn searches. Required for --blast option.

  --blast / --no-blast           Perform local blastn-short searches to
                                 extract alignment positions (default=FALSE)

  --help                         Show this message and exit.
```

Screen output example:

```
==== Run complete! ===
blastn output saved in OUT.blastn.txt
Table of alignment positions saved in OUT.alnpositions.tsv
Plot of alignment positions saved in OUT.alnpositions.pdf
```

blastn input/output (```-outfmt7```):
```
# Query: AB938103
# Database: User specified sequence set (Input: Zebrafish.12S.fasta)
# Fields: query acc.ver, subject acc.ver, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score
# 24 hits found
AB938103	NC_002333.2:1020-1971	93.750	16	1	0	2	17	249	264	0.008	24.3
AB938103	NC_002333.2:1020-1971	100.000	12	0	0	94	105	337	348	0.008	24.3
AB938103	NC_002333.2:1020-1971	89.474	19	2	0	38	56	285	303	0.032	22.3
AB938103	NC_002333.2:1020-1971	100.000	9	0	0	2	10	256	248	0.49	18.3
AB938103	NC_002333.2:1020-1971	100.000	9	0	0	49	57	476	468	0.49	18.3
AB938103	NC_002333.2:1020-1971	100.000	9	0	0	149	157	300	308	0.49	18.3
AB938103	NC_002333.2:1020-1971	100.000	9	0	0	64	72	332	340	0.49	18.3
```

TSV output - Reference sequence will always be on top:
```
Accession       Start   End
NC_002333.2:1020-1971   1       952
AB006953        1       945
AB015962        421     733
AB016274        547     637
AB018224        170     304
AB018225        170     304
AB018226        170     304
AB018227        150     305
AB018228        150     305
AB018229        150     305
AB018230        150     305
```

PDF output - Reference sequence will always be on top:
<img src="https://github.com/shenjean/mitohelper/blob/master/getalignment.sample.output.png" width="716" height="442">
