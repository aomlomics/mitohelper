# getMito, getSeq & getTaxa
getMito reference files:
- [mitofish.ref.tsv](https://drive.google.com/file/d/1q7VucLiOnR5L13KxPwIgKGKb70z-ffSO/view?usp=sharing) (630,974 records; NCBI nt: May 31 update; MitoFish: June 2 update)
- 12S.ref.tsv (27,642 records; NCBI nt: May 31 update; MitoFish: June 2 update; available in this repository)
- [COI.ref.tsv](https://drive.google.com/file/d/1q6RCVG3lKBVXuKBY-o8nwkpxJitaQ9kU/view?usp=sharing) (185,158 records; NCBI nt: May 31 update; MitoFish: June 2 update)

getSeq reference files (same database versions as above):
- [mitofish.pickle](https://drive.google.com/file/d/1qI5gPZydpHj5Fa_aQRbE2hoqlWnBr-JX/view?usp=sharing)
- [12S.pickle](https://drive.google.com/file/d/1qEp2DmXWiSWVZC4I3cxdYaJhrHont2xR/view?usp=sharing)
- COI.pickle (coming soon)

getTaxa reference file:
- [eukaryota.tsv](https://drive.google.com/file/d/1n3OtSwu6hC1DWXo6TJhZb9KL-yMma3ck/view?usp=sharing) (NCBI taxonomy: May 28 update)


## Wiki page: https://github.com/shenjean/getMito/wiki
## 1. About getMito
From a user-provided list of genera/species/subspecies, getMito extracts the corresponding GenBank accession numbers of their 12S rRNA sequences (reference file: <b>12S.ref.tsv</b>), cytochrome c oxidase subunit I (reference file: [COI.ref.tsv](https://drive.google.com/file/d/1q6RCVG3lKBVXuKBY-o8nwkpxJitaQ9kU/view?usp=sharing)), or mitochondrial sequences (reference file: [mitofish.ref.tsv](https://drive.google.com/file/d/1q7VucLiOnR5L13KxPwIgKGKb70z-ffSO/view?usp=sharing)), if available.  Visit the [wiki](https://github.com/shenjean/getMito/wiki) for more information.

## 2. About getSeq
getSeq is a companion script to getMito to fetch sequences from a getMito output file or a list of accession numbers. Sequence reference files are stored as python pickle dumps and include [mitofish.pickle](https://drive.google.com/file/d/1qI5gPZydpHj5Fa_aQRbE2hoqlWnBr-JX/view?usp=sharing), [12S.pickle](https://drive.google.com/file/d/1qEp2DmXWiSWVZC4I3cxdYaJhrHont2xR/view?usp=sharing), and COI.pickle. Visit the [wiki](https://github.com/shenjean/getMito/wiki) for more information.

## 3. About getTaxa
getTaxa is a companion script to getMito to fetch genus/species/subspecies belonging to a specified list of taxonomic categories (subfamily/family/order/class/phylum) using eukaryotic data from NCBI Taxonomy (reference file: [eukaryota.tsv](https://drive.google.com/file/d/1n3OtSwu6hC1DWXo6TJhZb9KL-yMma3ck/view?usp=sharing). The *.txt output can then be used as input for getMito. Visit the [wiki](https://github.com/shenjean/getMito/wiki) for more information.

## 4. Dependencies
- <b>.py</b> scripts: Python3 and the conda- and pip-installable [click](http://click.pocoo.org/5/) package
- <b>.ipynb</b> scripts: [Jupyter notebook](https://jupyter.org/) with Python3
- <b>getMito.sh</b>: Unix shell

## 5. Quick start
### I. getMito
 - python getMito.py -i <input_file> -o <output_prefix> -r <reference_file>
    - Example 1: python getMito.py -i input.txt -o OUT -r 12S.ref.tsv
    - Example 2: python getMito.py -i input.txt -o OUT -r mitofish.ref.tsv
    - Example 3: python getMito.py -i input.txt -o OUT -r COI.ref.tsv
 - getMito.sh <input_file> <output_prefix> <reference_database>
 - getMito.ipynb: Click "Run" on last cell in notebook, and type each of the required three inputs sequentially in the whitebox below the cell, followed by the "Enter" key.

### II. getSeq
 - python getSeq.py -i <input_file> -t <input_file_type: getmito or plain> -r <reference file> -o <output_file> 
  - Example 1: python getSeq.py -i OUT_species.hits.tsv -t getmito -r 12S.pickle -o OUT.fasta
  - Example 2: python getSeq.py -i accession.txt -t plain -r mitofish.pickle -o output.fasta
 - getSeq.ipynb: Click "Run" on last cell in notebook, and type each of the required two inputs sequentially in the whitebox below the cell, followed by the "Enter" key.

### III. getTaxa
 - python getTaxa.py -i <input_file> -o <output_prefix> 
 - getTaxa.ipynb: Click "Run" on last cell in notebook, and type each of the required two inputs sequentially in the whitebox below the cell, followed by the "Enter" key.
 

## 5. Input files:
### I. getMito
Plain text file, with each line containing a genera, species, or subspecies, e.g.:
```
Histioteuthis celetaria celetaria
Histioteuthis corona corona
Stomias boa boa
Lampadena urophaos atlantica
```
### II. getSeq
Input can be any output file of getMito <i>(-t getmito)</i>:
```
Stomias boa     species KX929921      Stomias boa voucher ZMUC P2014774 12S ribosomal RNA gene, partial sequence; mitochondrial
Stomias boa     species LC458106      Stomias boa mitochondrial gene for 12S rRNA, partial sequence
Lampadena urophaos      species LC026535      Lampadena urophaos urophaos mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: HUMZ:220996
Lampadena urophaos      species LC026536      Lampadena urophaos urophaos mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: HUMZ:221119
Lampadena urophaos      species LC146002      Lampadena urophaos mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: CBM:ZF:14569
```
Input can also be a plain text file containing a list of accession numbers <i>(-t plain)</i>:
```
AY484973
AY484974
HM114425
HM114426
HM114427
```


### III. getTaxa
Tab-separated file with the fields: family/order/class/phylum name, input taxonomic level, and desired output taxonomic level. 
Input is not case-sensitive, e.g.:
```
bathylagidae    family  species
Onychoteuthidae family  species
Anguilliformes  order   species
Astronesthes    order   subspecies
Melamphaes      order   subspecies
Lepidosauria    class   subspecies
```
## Output files:
### I. getMito
Tab-separated output file(s) with the following fields: Query, taxonomic level, GenBank accession number, gene description. 

<br>Example output file <<i>OUT_species.hits.tsv</i>>:
```
Stomias boa     species KX929921      Stomias boa voucher ZMUC P2014774 12S ribosomal RNA gene, partial sequence; mitochondrial
Stomias boa     species LC458106      Stomias boa mitochondrial gene for 12S rRNA, partial sequence
Lampadena urophaos      species LC026535      Lampadena urophaos urophaos mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: HUMZ:220996
Lampadena urophaos      species LC026536      Lampadena urophaos urophaos mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: HUMZ:221119
Lampadena urophaos      species LC146002      Lampadena urophaos mitochondrial gene for 12S rRNA, partial sequence, specimen_voucher: CBM:ZF:14569
```
getMito output files can include <output_prefix>_genus.hits.tsv, <output_prefix>_species.hits.tsv, and <output_prefix>_subspecies.hits.tsv, depending on the taxonomic categories of hits produced.

### II. getSeq
Outputs standard fasta file with accession numbers in header lines:
```
>AY484973
AAAAAGCTTCAAACTGGGATTAGATACCCCACTATGCTTAGCCCTAAACCTCAACAGTTAAATCAACAAAACTGCTCGCCAGAACACTACGAGCCACAGCTTAAAACTCAAAGGACCTGGCGGTGCTTCATATCCCTCTAGAGGAGCCTGTTCTGTAAT
CGATAAACCCCGATCAACCTCACCACCTCTTGCTCAGCCTATATACCGCCATCTTCAGCAAACCCTGATGAAGGCTACAAAGTAAGCGCAAGTACCCACGTAAAGACGTTAGGTCAAGGTGTAGCCCATGAGGTGGCAAGAAATGGGCTACATTTTCTA
CCCCAGAAAACTACGATAGCCCTTATGAAACTTAAGGGTCGAAGGTGGATTTAGCAGTAAACTGAGAGTAGAGTGCTTAGTTGAACAGGGCCCTGAAGCGCGTACACACCGCCCCGTCACCCCTCTGCAGTCA
>AY484974
AAAAAGCTTCAAACTGGGATTAGATACCCCACTATGCTTAGCCCTAAACCTCAACAGTTAAATCAACAAAACTGCTCGCCAGAACACTACGAGCCACAGCTTAAAACTCAAAGGACCTGGCGGTGCTTCATATCCCTCTAGAGGAGCCTGTTCTGTAAT
CGATGAACCCCGATCAACCTCACCACCTCTTGCTCAGCCTATATACCGCCATCTTCAGCAAACCCTGATGAAGGCTACAAAGTAAGCGCAAGTACCCACGTAAAGACGTTAGGTCAAGGTGTAGCCCATGAGGTGGCAAGAAATGGGCTACATTTTCTA
CCCCAGAAAACTACGATAGCCCTTATGAAACTTAAGGGTCGAAGGTGGATTTAGCAGTAAACTGAGAGTAGAGTGCTTAGTTGAACAGGGCCCTGAAGCGCGTACACACCGCCCGTCACCCTCTGCAGTCA
```

### III. getTaxa 
<output_prefix>_taxa.tsv is tab-separated with the following fields: family/order/class/phylum name, input taxonomic level, genus/species/subspecies hit and output taxonomic level, e.g.:
```
Bathylagidae    family  Lipolagus ochotensis    species
Bathylagidae    family  Bathylagus euryops      species
Bathylagidae    family  Bathylagus stilbius     species
Lepidosauria    class   Lacerta trilineata polylepidota subspecies
Lepidosauria    class   Lacerta media wolterstorffi     subspecies
Lepidosauria    class   Lacerta trilineata major        subspecies
```
<output_prefix>_taxa.txt is a plain-text file containing all hits and can be used as the inputfile for getMito, e.g.:
```
Lipolagus ochotensis
Bathylagus euryops
Bathylagus stilbius
```
