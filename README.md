# getMito

The [getMito Wiki page](https://github.com/shenjean/getMito/wiki) describes the creation of reference database files. 

```
Usage: getMito.py [OPTIONS]

From a user-provided list of fish taxonomic names, getMito extracts 
available mitochondrial information and FASTA file (optional) at user-specified taxonomic levels. 
The reference database is prepared from the MitoFish database and NCBI (Jul 2020 update).

Options:
  -i, --input_file TEXT           Input query file (e.g. input.txt) [required]
  -o, --output_prefix TEXT        Output prefix (e.g. OUT)  [required]
  -d, --database_file TEXT        Database file (e.g. mitofish.all.Jul2020.tsv) [required]
  -l, --tax_level [1|2|3|4|5|6|7] The taxonomic level of the search (e.g. 7 for species search, 6 for genus search)
  --fasta / --no-fasta            Generate FASTA file containing sequences of all matching hits (default=FALSE)
  --help                          Show this message and exit.

Dependencies: Python3 and the conda- and pip-installable click package
```
Reference database files:
- [mitofish.all.Jul2020.tsv](https://drive.google.com/uc?export=download&id=1C1vzqBpC7jsDfgyepbYS2vqDGBYf3rwY) (639,987 records; Jul 2020 update)
- [mitofish.12S.Jul2020.tsv](https://drive.google.com/uc?export=download&id=1CqG7AoShzAD2JwnoU_bRabuShOR1CvqO) (34,558 records)
- [mitofish.COI.Jul2020.tsv](https://drive.google.com/uc?export=download&id=1CpuBkOEEweIKUVCZ6Ueq3JFyTvj4IVQy) (189,956 records)

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
