#!/usr/bin/env bash

month=Mar2022

# Search for 12S genes and complete mitogenomes from main mitohelper reference file

echo "Processing 12S..."

grep -i -e "12S ribo" -e "12S rRNA" -e "12S small" \
-e "complete genome" -e "complete mito"  \
mitofish.all."$month".tsv >mitofish.12S.partI.tsv

# Extract 12S genes from other studies with NCBI records that may not contain the keywords above 

#sed "s/^/\^/" 12S.unconventional.acc >12S.unconventional.grep 

#for i in `cat 12S.unconventional.grep`
#do
#grep -m 1 $i mitofish.all."$month".tsv >>mitofish.12S.unconventional.tsv
#done

# Combine 12S datasets and de-duplicate

cat mitofish.12S.partI.tsv mitofish.12S.unconventional.tsv | sort | uniq >mitofish.12S.noheader.tsv
cat mitofish.header mitofish.12S.noheader.tsv >mitofish.12S."$month".tsv

# Extract COI hits and filter out cytochrome b records

echo "Processing COI..."

grep -i -e "(COI)" -e "CO1" -e "cytochrome c oxidase subunit I " \
-e "cytochrome c oxidase subunit 1" -e "COI " -e "complete genome" -e "complete mito" \
-e "COX1" -e "(COXI)" -e "cytochrome oxidase subunit I " mitofish.all."$month".tsv \
| grep -v -i "cytochrome b" | grep -v -i "cytb"  >mitofish.COI.partI.tsv

# Extract COI records that may not contain the keywords above 
#grep -f COI.unconventional.acc mitofish.all."$month".tsv >mitofish.COI.unconventional.tsv

# Combine COI datasets and de-duplicate
cat mitofish.header mitofish.COI.partI.tsv mitofish.COI.unconventional.tsv >mitofish.COI."$month".tsv
