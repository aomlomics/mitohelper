# Mitohelper

**Citation**
> Jean Lim, S, Thompson, LR. Mitohelper: A mitochondrial reference sequence analysis tool for fish eDNA studies. Environmental DNA. 2021; 00: 1– 10.  https://doi.org/10.1002/edn3.187


**Mitohelper** is a Python-based mitochondrial reference sequence analysis tool for fish eDNA studies. It is useful for researchers interested in:

- finding out whether mitochondrial reference sequences exist for specific fish species/taxonomy (`getrecord` command in `mitohelper.py`)
- finding out which specific region of a mitochondrial gene has been sequenced (by aligning with a reference sequence) (`getalignment` command in  `mitohelper.py`)
- using pre-formatted QIIME-compatible ribosomal RNA (12S or 12S+16S+18S) sequence and taxonomy databases for downstream analysis (available in the `QIIME-compatible` folder) 
- knowing more about our data processing pipeline and mitohelper algorithm (visit the [DevWiki](https://github.com/aomlomics/mitohelper/wiki/) for all the nitty gritty details!)


Dependencies
----

> - Tested on python 3.6.10
> - For local blastn searches, [NCBI BLAST+ executables](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) (specifically `blastn`) must be installed and in the system path


Required python modules:
- click (v7.1.2)
- matplotlib (v3.3.4)
- pandas (v0.25.3)
- seaborn (v0.10.1)

  Installation:
  - pip:  
    ```
    pip install -r requirements.txt
    ```
  - conda:  
    ```
    conda install --file requirements.txt
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

`mitohelper.py getrecord --help`

```
Usage: mitohelper.py getrecord [OPTIONS]

  Retrieve fish mitochondrial records from taxa list

Options:
  -i, --input_file TEXT           Input query file (e.g. input.txt)
                                  [required]

  -o, --output_prefix TEXT        Output prefix (e.g. OUT)  [required]
  -d, --database_file TEXT        Database file (e.g.
                                  mitofish.all.Mar2021.tsv)  [required]

  -l, --tax_level [1|2|3|4|5|6|7]
                                  The taxonomic level of the search (e.g 7 for
                                  species, 6 for genus etc)

  --fasta / --no-fasta            Generate FASTA file output containing
                                  sequences of all matching hits
                                  (default=FALSE)

  --taxout / --no-tax             Generate taxonomy file output for all
                                  matching hits (default=FALSE)

  --help                          Show this message and exit

```

> Reference database files can be downloaded from [<img src=https://zenodo.org/badge/DOI/10.5281/zenodo.15028392.svg>](https://doi.org/10.5281/zenodo.15028392)
> - mitofish.all.Mar2025.tsv (883,519 records)
> - mitofish.12S.Mar2025.tsv (61,379 records of 12S rRNA gene >50 bp long)
> - mitofish.12S.Mar2025_NR.fasta (FASTA file of 12S rRNA gene records)
> - mitofish.COI.Mar2025.tsv (323,337 records)

- Usage example:
```
mitohelper.py getrecord -i testdata/species.query.txt -o testdata/getrecordOUT -d mitofish.all.Sep2023.tsv -l 7 --fasta --taxout
```

- Input file example (`testdata/species.query.txt`):

```
Abraliopsis pfefferi
Ahliesaurus berryi
Alepisaurus FEROX
anotopterus pharao
AHLIESAURUS BERRYI
```

- Screen output:

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
Output taxonomy file saved in testdata/getrecordOUT_L7.taxonomy.tsv
```

- Output TSV file columns and example (`testdata/getrecordOUT_L7_hits.tsv`):
> 1. Query
> 2. Accession - NCBI accession 
> 3. Gene definition - Gene definition in GenBank record
> 4. taxid - NCBI taxonomy ID
> 5. Superkingdom
> 6. Phylum
> 7. Class
> 8. Order
> 9. Family
> 10. Genus
> 11. Species
> 12. Sequence
> 13. OrderID - Order classification in ["Fishes of the World, 5th edition" (Nelson et al. 2016)](https://www.wiley.com/en-us/Fishes+of+the+World%2C+5th+Edition-p-9781118342336)
> 14. FamilyID - Family classification in ["Fishes of the World, 5th edition" (Nelson et al. 2016)](https://www.wiley.com/en-us/Fishes+of+the+World%2C+5th+Edition-p-9781118342336)

```
Query   Accession       Gene definition taxid   Superkingdom    Phylum  Class   Order   Family  Genus   Species Sequence        OrderID FamilyID
Ahliesaurus berryi      EU366544        Ahliesaurus berryi voucher MCZ 161662 cytochrome oxidase subunit I (COI) gene, partial cds; mitochondrial       509771  Eukaryota       Chordata        Actinopteri     Aulopiformes    Notosudidae     Ahliesaurus     Ahliesaurus berryi      GTGAACATGAGGTGGGCTCAGACGATAAAGCCTAGGAGGCCGATTGCTATCATAGCTCAGACCATGCCCATGTAGCCAAAGGGTTCTTTTTTCCCTGAATAGTAGGCTACGATGTGGGAGATCATACCAAAGCCGGGGAGAATAAGAATGTAGACCTCTGGGTGACCAAAGAATCAGAACAGGTGCTGGTAAAGGATGGGGTCTCCGCCCCCTGCCGGGTCAAAGAAGGTGGTGTTCAGGTTTCGGTCAGTTAGAAGTATTGTAATGCCTGCCGCTAGAACGGGGAGGGAGAGTAAAAGAAGGACGGCAGTAATAAGGACTGCTCAGACGAAGAGGGGAGTTTGGTACTGGGTGATGGCGGGGGGTTTTATGTTAATAATTGTTGTGATGAAGTTAATGGCACCCAGGATAGAGGAGATACCTGCCAGGTGGAGGGAGAAGATGGTTAGGTCTACGGAAGCTCCTGCATGGGCCAGGTTGCTGGCGAGAGGCGGATACACAGTTCATCCTGTTCCGGCCCCGGCTTCTACAGCGGAGGAGGCTAGGAGTAGAAGGAAGGATGGGGGGAGTAGTCAAAAGCTCATGTTGTTCATTCGGGGGAATGCCATGTCAGGCGCCCCGATCATAAGAGGGATAAGTCAGTTTCCGAACCCACCGATCATAATTGGTATTACCATGAAAAAAATTATTACGAAAGCGTGGGCAGTAACGATAACATTGTAAATCTGGTCGTCTCCTAAAAGGGCTCCGGGTTGGCTTAGCTCAGCTCGGATGAGAAGGCT  44      214
Ahliesaurus berryi      KF929574        Ahliesaurus berryi voucher KUT 5285 cytochrome oxidase subunit 1 (COI) gene, partial cds; mitochondrial 509771  Eukaryota       Chordata        Actinopteri     Aulopiformes    Notosudidae     Ahliesaurus     Ahliesaurus berryi      CCTCTACCTACTATTTGGTGCCTGGGCCGGGATGGTGGGTACAGCCCTAAGCCTTCTCATCCGAGCTGAGCTAAGCCAACCCGGAGCCCTTTTAGGAGACGACCAGATTTACAATGTTATCGTTACTGCCCACGCTTTCGTAATAATTTTTTTCATGGTAATACCAATTATGATCGGTGGGTTCGGAAACTGACTTATCCCTCTTATGATCGGGGCGCCTGACATGGCATTCCCCCGAATGAACAACATGAGCTTTTGACTACTCCCCCCATCCTTCCTTCTACTCCTAGCCTCCTCCGCTGTAGAAGCCGGGGCCGGAACAGGATGAACTGTGTATCCGCCTCTCGCCAGCAACCTGGCCCATGCAGGAGCTTCCGTAGACCTAACCATCTTCTCCCTCCACCTGGCAGGTATCTCCTCTATCCTGGGTGCCATTAACTTCATCACAACAATTATTAACATAAAACCCCCCGCCATCACCCAGTACCAAACTCCCCTCTTCGTCTGAGCAGTCCTTATTACTGCCGTCCTTCTTTTACTCTCCCTCCCCGTTCTAGCGGCAGGCATTACAATACTTCTAACTGACCGAAACCTGAACACCACCTTCTTTGACCCGGCAGGGGGCGGAGACCCCATCCTTTACCAGCACCTG    44      214
```
- Output taxonomy file example (`testdata/getrecordOUT_L7_taxonomy.tsv`):
> The output taxonomy file can be directly imported into [QIIME 2](https://qiime2.org)
```
Feature ID      Taxon
EU366544        d__Eukaryota; p__Chordata; c__Actinopteri; o__Aulopiformes; f__Notosudidae; g__Ahliesaurus; s__Ahliesaurus berryi
KF929574        d__Eukaryota; p__Chordata; c__Actinopteri; o__Aulopiformes; f__Notosudidae; g__Ahliesaurus; s__Ahliesaurus berryi
AF092181        d__Eukaryota; p__Chordata; c__Actinopteri; o__Aulopiformes; f__Alepisauridae; g__Alepisaurus; s__Alepisaurus ferox
AP004211        d__Eukaryota; p__Chordata; c__Actinopteri; o__Aulopiformes; f__Alepisauridae; g__Alepisaurus; s__Alepisaurus ferox
EU366542        d__Eukaryota; p__Chordata; c__Actinopteri; o__Aulopiformes; f__Alepisauridae; g__Alepisaurus; s__Alepisaurus ferox
```

getalignment
----

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

- Usage example:

```
mitohelper.py getalignment -i testdata/12S.test.fasta -o testdata/blastnALN -r testdata/Zebrafish.12S.ref.fasta --blastn-task blastn
```

- Screen output:

```
==== Run complete! ===
blastn output saved in blastnALN.blastn.txt
Table of alignment positions saved in blastnALN.alnpositions.tsv
Plot of alignment positions saved in blastnALN.alnpositions.pdf
```

- blastn `-outfmt 7` input/output (`testdata/blastnALN.blastn.txt`):

```
# BLASTN 2.6.0+
# Query: NC_002333.2:1020-1971 Danio rerio mitochondrion, complete genome
# Database: User specified sequence set (Input: Zebrafish.12S.ref.fasta)
# Fields: query acc.ver, subject acc.ver, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score
# 1 hits found
NC_002333.2:1020-1971   NC_002333.2:1020-1971   100.000 952     0       0       1       952     1       952     0.0     1718
```

- Graphical output with reference sequence on top (`testdata/blastnALN.alnpositions.pdf`):

<img src="https://github.com/aomlomics/Mitohelper/blob/master/testdata/getalignment_out.PNG" width="807" height="481.8">

- Tab-separated output (`testdata/blastnALN.alnpositions.tsv`):

*Reference sequence will always be on top.*

```
Accession       Start   End     Bit_Score
NC_002333.2:1020-1971   1       952     1718
AB938103        249     348     37
AB006953        1       945     1099
AB015962        102     945     484
AB016274        17      945     549
AB018224        2       825     473
AB018225        2       804     471
AB018226        1       825     491
AB018227        1       804     520
AB018228        1       825     504
AB018229        1       804     506
AB018230        1       825     513
```




