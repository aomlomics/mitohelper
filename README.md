# mitohelper

**mitohelper** is a repository built to facilitate experimental design, alignment visualization, and reference sequence analysis in fish eDNA studies. It is useful for researchers who are interested in:

- finding out whether mitochondrial reference sequences exist for specific fish species/taxonomy (`getrecord` command in `mitohelper.py`)
- finding out which specific region of a mitochondrial gene has been sequenced (by aligning with a reference sequence) (`getalignment` command in  `mitohelper.py`)
- using pre-formatted QIIME-compatible ribosomal RNA (12S or 12S+16S+18S) sequence and taxonomy databases for downstream analysis (available in the `QIIME-compatible` folder) 
- knowing more about our data processing pipeline and mitohelper algorithm (visit the [DevWiki](https://github.com/shenjean/mitohelper/wiki/) for all the nitty gritty details!)

Dependencies
----

> - Tested on python 3.6.10
> - For local blastn searches, NCBI [BLAST+ executables](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) (specifically `blastn`) must be installed and in the system path

```
Required python modules
- click (v7.1.2)
- matplotlib (v3.3.0)
- pandas (v0.25.3)
- seaborn (v0.10.1)
```

Usage
----

`mitohelper.py --help`

```
Usage: mitohelper.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  getalignment  Pairwise align input sequences against a reference
  getrecord     Retrieve fish mitochondrial records from taxa list
```

getrecord
----

`mitohelper.py getrecord --help`

```
Usage: mitohelper.py getrecord [OPTIONS]

  Retrieve fish mitochondrial records from taxa list

Options:
  -i, --input_file TEXT           Input query file (e.g. input.txt)
                                  [required]

  -o, --output_prefix TEXT        Output prefix (e.g. OUT)  [required]
  -d, --database_file TEXT        Database file (e.g. mitofish.all.Sep2020.tsv
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
> - [mitofish.all.Oct2020.tsv](https://drive.google.com/uc?export=download&id=1vBPouxanNWYvmp7sWsl9ZH09IE0GflL-) (650,841 records; Oct 2020 update)
> - [mitofish.12S.Oct2020.tsv](https://drive.google.com/uc?export=download&id=1vdECwfTJLxZ0ewfyeeeMDBXkdzlsl0MO) (34,729 records)
> - [mitofish.COI.Oct2020.tsv](https://drive.google.com/uc?export=download&id=1v4XxK9mnple64aHS-cvDY5OOxem9cl6p) (204,804 records)

Usage example:
```
python mitohelper.py getrecord -i testdata/species.query.txt -o testdata/getrecordOUT -d mitofish.all.Aug2020.tsv -l 7 --fasta
```

Input file example (`species.query.txt` in folder `testdata`):

```
Abraliopsis pfefferi
Ahliesaurus berryi
Alepisaurus FEROX
anotopterus pharao
AHLIESAURUS BERRYI
```

Screen log:

```
=== Searching query #1: <Abraliopsis pfefferi> ===
=== Searching query #2: <Ahliesaurus berryi> ===
Search string:Ahliesaurus berryi	Taxonomic level:L7	Hits:2
=== Searching query #3: <Alepisaurus FEROX> ===
Search string:Alepisaurus ferox	Taxonomic level:L7	Hits:32
=== Searching query #4: <anotopterus pharao> ===
Search string:Anotopterus pharao	Taxonomic level:L7	Hits:9
=== Searching query #5: <AHLIESAURUS BERRYI> ===
DUPLICATE WARNING: Query has already been processed!
==== Run complete! ===
Accession numbers of subspecies hits and description saved in testdata/getrecordOUT_L7_hits.tsv
FASTA-formatted sequences saved in testdata/getrecordOUT_L7.fasta
```

Output TSV file example (`getrecordOUT_L7_hits.tsv` in folder `testdata`):

```
Query   Accession       Gene definition txid    Superkingdom    Phylum  Class   Order   Family  Genus   Species Sequence
Ahliesaurus berryi      EU366544        Ahliesaurus berryi voucher MCZ 161662 cytochrome oxidase subunit I (COI) gene, partial cds; mitochondrial       509771  Eukaryota       Chordata        Actinopteri     Aulopiformes    Notosudidae     Ahliesaurus     Ahliesaurus berryi      GTGAACATGAGGTGGGCTCAGACGATAAAGCCTAGGAGGCCGATTGCTATCATAGCTCAGACCATGCCCATGTAGCCAAAGGGTTCTTTTTTCCCTGAATAGTAGGCTACGATGTGGGAGATCATACCAAAGCCGGGGAGAATAAGAATGTAGACCTCTGGGTGACCAAAGAATCAGAACAGGTGCTGGTAAAGGATGGGGTCTCCGCCCCCTGCCGGGTCAAAGAAGGTGGTGTTCAGGTTTCGGTCAGTTAGAAGTATTGTAATGCCTGCCGCTAGAACGGGGAGGGAGAGTAAAAGAAGGACGGCAGTAATAAGGACTGCTCAGACGAAGAGGGGAGTTTGGTACTGGGTGATGGCGGGGGGTTTTATGTTAATAATTGTTGTGATGAAGTTAATGGCACCCAGGATAGAGGAGATACCTGCCAGGTGGAGGGAGAAGATGGTTAGGTCTACGGAAGCTCCTGCATGGGCCAGGTTGCTGGCGAGAGGCGGATACACAGTTCATCCTGTTCCGGCCCCGGCTTCTACAGCGGAGGAGGCTAGGAGTAGAAGGAAGGATGGGGGGAGTAGTCAAAAGCTCATGTTGTTCATTCGGGGGAATGCCATGTCAGGCGCCCCGATCATAAGAGGGATAAGTCAGTTTCCGAACCCACCGATCATAATTGGTATTACCATGAAAAAAATTATTACGAAAGCGTGGGCAGTAACGATAACATTGTAAATCTGGTCGTCTCCTAAAAGGGCTCCGGGTTGGCTTAGCTCAGCTCGGATGAGAAGGCT
```

getalignment
----
Graphical output with reference sequence on top:

<img src="https://github.com/shenjean/mitohelper/blob/master/testdata/getalignment_out.PNG" width="807" height="481.8">

`mitohelper.py getalignment --help`

```
Usage: mitohelper.py getalignment [OPTIONS]

  Pairwise align input sequences against a reference

Options:
  -i, --input_file TEXT           Input file: either blastn output file or
                                  FASTA file  [required]
  -o, --output_prefix TEXT        Output prefix (e.g. OUT)  [required]
  -r, --reference_sequence TEXT   FASTA file of a single reference sequence
                                  for blastn searches. Required for --blast
                                  option.
  --blastn-task [blastn|blastn-short|megablast|dc-megablast|none]
                                  Choice of blastn task for local similarity
                                  searches used to extract alignment positions
                                  [default:blastn-short]  [required]
  --help                          Show this message and exit.

```

Usage example:

```
python mitohelper.py getalignment -i testdata/12S.test.fasta -o testdata/blastnALN -r testdata/Zebrafish.12S.ref.fasta --blastn-task blastn
```

Screen log:

```
==== Run complete! ===
blastn output saved in blastnALN.blastn.txt
Table of alignment positions saved in blastnALN.alnpositions.tsv
Plot of alignment positions saved in blastnALN.alnpositions.pdf
```

blastn `-outfmt 7` input/output (`alignmentOUT.blastn.txt` in folder `testdata`):

```
# BLASTN 2.9.0+
# Query: NC_002333.2:1020-1971 Danio rerio mitochondrion, complete genome
# Database: User specified sequence set (Input: Zebrafish.12S.ref.fasta)
# Fields: query acc.ver, subject acc.ver, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score
# 1 hits found
NC_002333.2:1020-1971   NC_002333.2:1020-1971   100.000 952     0       0       1       952     1       952     0.0     1718
```

Tab-separated output (`blastnALN.alnpositions.tsv` in folder `testdata`):

*Reference sequence will always be on top.*

```
Accession       Start   End     Bit_Score
NC_002333.2:1020-1971   1       952     37
AB938103        249     348     1099
AB006953        1       945     484
AB015962        102     945     550
AB016274        17      945     473
AB018224        2       825     471
AB018225        2       804     491
AB018226        1       825     520
AB018227        1       804     505
AB018228        1       825     506
AB018229        1       804     513
AB018230        1       825     513
```

Graphical output (`blastnALN.alnpositions.pdf` in folder `testdata`):


