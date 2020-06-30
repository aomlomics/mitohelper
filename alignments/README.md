### Reference alignments ###

I. <b>Seed alignments</b> are created from whole mitogenome sequences downloaded from [MitoFish](http://mitofish.aori.u-tokyo.ac.jp/). Alignments were created using ClustalW using default parameters.
- 12S.seed.aligned.fasta
- COI.seed.aligned.fasta

II. <b>Full-length 12S rRNA gene and COI gene alignments</b> are created using the full sequence dataset, using the seed alignments as template. [Mothur](http://mothur.org) v1.42.1 was used to create the alignments. 
```
align.seqs(candidate=12S.ref.fasta,template=12S.seed.aligned.fasta,flip=t,processors=10)
```

III. <b>Alignments for meta-barcoding amplicon regions</b> are truncated from full-length alignments and manually inspected in BioEdit v7.2.5. These alignments include the primer sequences, where available. Sequences <50bp were removed from the truncated alignment using Mothur:

```
summary.seqs(fasta=12S.V5.raw.align,processors=10)
screen.seqs(minlength=50)
summary.seqs()"
```
- 12S.mifish.align.fasta contains region amplified by [MiFish primers](https://royalsocietypublishing.org/doi/10.1098/rsos.150088) GTGTCGGTAAAACTCGTGCCAGC (MiFish-U-F) and CATAGTGGGGTATCTAATCCCAGTTTG (MiFish-U-R).

- 12S.V5.align.fasta contains region amplified by [V5 primers](https://www.frontiersin.org/articles/10.3389/fmars.2020.00226/full)  ACTGGGATTAGATACCCC (ECO-V5-F)/ACTGGGATTAGATAC CCT (ECO-V5-SF) and TAGAACAGGCTCCTCTAG (ECO-V5-R)
