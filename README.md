# getMito & getTaxa
## 1. getMito
From a user-provided list of genera/species/subspecies, <b>getMito</b> extracts the corresponding GenBank accession numbers of their 12S rRNA sequences (reference file: <b>12S.ref.tsv</b>) or mitochondrial sequences (reference file: [mitofish.ref.tsv](https://drive.google.com/file/d/176hJjezjGTdGL3wYu4yM7nPmUV57Oiav/view?usp=sharing)), if available.  Refer to the [wiki](https://github.com/shenjean/getMito/wiki) for more information.

## 2. getTaxa
getTaxa is a companion script to getMito to fetch genus/species/subspecies belonging to a specified list of taxonomic categories (family/order/class/phylum) using data from [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/Taxonomy). The *.txt output can then be used as input for getMito. Refer to the [wiki](https://github.com/shenjean/getMito/wiki) for more information.

## 3. Dependencies
- For .py scripts: Python3 and the conda- and pip-installable [click](http://click.pocoo.org/5/) package
- For .ipynb scripts: Jupyter notebook with Python3
- For getMito.sh: Unix shell

## 4. Quick start
### 1. getMito
 - python getMito.py -i <input_file> -o <output_prefix> -r <reference database: 12S.ref.tsv or mitofish.ref.tsv>
 - Example 1: python getMito.py -i input.txt -o OUT -r 12S.ref.tsv
 - Example 2: python getMito.py -i input.txt -o OUT -r mitofish.ref.tsv
 - getMito.sh <input_file> <output_prefix> <reference_database>
 - getMito.ipynb: Click "Run" on last cell in notebook, and type each of the required three inputs sequentially in the whitebox below the cell, followed by the "Enter" key.

### 2. getTaxa
 - python getTaxa.py -i <input_file> -o <output_prefix> 
 - getTaxa.ipynb: Click "Run" on last cell in notebook, and type each of the required two inputs sequentially in the whitebox below the cell, followed by the "Enter" key.
 

## getMito input file:
Plain text file, with each line containing a genera, species, or subspecies. Test data are in the <b>fishdata</b> subfolder. <br>
e.g.
```
Histioteuthis celetaria celetaria
Histioteuthis corona corona
Stomias boa boa
Lampadena urophaos atlantica
```
## getMito reference files:
Reference files were prepared from downloaded <b>MitoFish (Apr 2 2020 update</b>) and <b>NCBI data (Apr 12 2020 version</b>). For data preparation pipeline, refer to <i>getMito.ipynb</i>, or the the [getMito wiki](https://github.com/shenjean/getMito/wiki). 

A user can choose from two reference files:
1. <b>12S.ref.tsv</b> - Tab-separated list of NCBI acession numbers and gene description for 12S rRNA genes. Available here.
2. <b>mitofish.ref.tsv</b> - Tab-separated list of NCBI acession numbers and gene description for mitochondrial genes/genomes. Due to GitHub's file size limitation, this file (~502 MB) could not be uploaded here. Download from [here](https://drive.google.com/file/d/176hJjezjGTdGL3wYu4yM7nPmUV57Oiav/view?usp=sharing) instead.

## getMito output files:
Output files are tab-separated with the following fields: Query, taxonomic level, GenBank accession number, gene description

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

