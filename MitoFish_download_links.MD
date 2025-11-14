## MitoFish

MitoFish sequence data can be downloaded from `https://mitofish.aori.u-tokyo.ac.jp/download/fullseq/latest/mitofishdb.fa.gz` 

It is a `gzipped` FASTA file rather than `zip`.

**Sequence Title**

For each sequence, the title only contains GenBank accessions, such as:

```
>AB374153
CAGAAAGAAGATTATAAACCCACCCCTACCCAGAAAGAAGATTATAAACCCACCCCTACCCACAAAG
AAAGGAGATTCTAACTCCCACCCCTAACTCCCAAAGCTAGGATTCTAAGCTAAACTATTCTTTG
```

However, if multiple accessions share identical sequences, they are combined into one entry, separated by ';', such as:
```
>OR134897;OR134896
CCCTTTACTTAGTATTTGGTGCATGAGCCGGAATAGTTGGCACAGCTCTTAGCCTCTTAATCCGGGCC
GAGCTAAGCCAACCCGGCTCCCTACTAGGTGACGACCAGATCTACAATGTCATCGTTACTGCACACGC
ATTCGTGATAATTTTCTTTATAGTAATGCCAATTATGATTGGAGGCTTTGGGAACTGACTAGTACCCCTT
ATGATCGGAGCACCAGACATGGCATTTCCACGAATAAATAACATGAGCTTCTGACTACTCCCCCCATCA
TTCCTGCTTCTCCTAGCCTCTTCCGGCGTTGAAGCGGGGGCTGGAACAGGTTGAACTGTATACCCACC
CCTTGCCGGCAACCTCGCCCATGCGGGAGCCTCAGTTGATTTAACCATCTTCTCACTACATCTGGCCG
GTGTTTCCTCAATCCTAGGGGCAATCAACTTCATTACCACAATTATTAACATGAAACCCCCAGCCATCTC
CCAATACCAAACCCCCCTATTCGTCTGAGCTGTACTCATTACAGCCGTCTTACTTCTCCTTTCATTACCA
GTCCTAGCTGCCGGCATTACAATGCTGCTAACAGACCGAAATTTAAACACCACCTTCTTCGACCCTGCA
GGAGGGGGAGACCCAATTTTATACCAACACTTGTTC
``` 
which means OR134897 and OR134896 share identical sequences

## Mitohelper
Mitohelper reference database files can be downloaded from [<img src=https://zenodo.org/badge/DOI/10.5281/zenodo.17602902.svg>](https://doi.org/10.5281/zenodo.17602902)

> **Nov2025 update**: The MitoFish database underwent a major update since September 30th (UTC + 9) where duplicated records were combined into one entry. The Nov2025 version of Mitohelper's reference datasets was de-deduplicated based on updated records in the September 30th version of the MitoFish database.
> - mitofish.all.Nov.2025.tsv (558,313 de-duplicated records)
> - mitofish.12S.Mar2025.tsv (64,059 records of 12S rRNA gene >50 bp long)
> - mitofish.12S.Mar2025_NR.fasta (FASTA file of 12S rRNA gene records)
> - mitofish.COI.Mar2025.tsv (200,911 de-duplicated records)
