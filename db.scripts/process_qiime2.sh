#!/usr/bin/env bash

month=Mar2022

# Download and export QIIME-compatible SILVA NR99 full-length sequences and taxonomy
# wget https://data.qiime2.org/2020.11/common/silva-138-99-seqs.qza
# wget https://data.qiime2.org/2020.11/common/silva-138-99-tax.qza
# qiime tools export --input-path silva-138-99-seqs.qza --output-path silva138.99.seq
# qiime tools export --input-path silva-138-99-tax.qza --output-path silva138.99.tax

echo "Convert mitofish 12S table into FASTA file.."
cat mitofish.12S."$month".tsv | awk -F "\t" '{OFS="#"}{print $1,$11}' | grep -v "Accession#Sequence" | sed "s/^/>/" | tr "#" "\n" >mitofish.12S."$month".fasta

echo "Extract list of accession numbers (feature IDs).."
cut -f1 mitofish.12S."$month".tsv | sed "s/Accession/Feature ID/" >12S.featureID

echo "Extract taxonomic information (domain through species).."
cut -f6 mitofish.12S."$month".tsv | sed "s/^/d__Eukaryota; p__Chordata; c__/" | sed "s/$/;/" >12S.class
cut -f7 mitofish.12S."$month".tsv | sed "s/^/o__/" | sed "s/$/;/" >12S.order
cut -f8 mitofish.12S."$month".tsv | sed "s/^/f__/" | sed "s/$/;/" >12S.family
cut -f9 mitofish.12S."$month".tsv | sed "s/^/g__/" | sed "s/$/;/" >12S.genus
cut -f10 mitofish.12S."$month".tsv | sed "s/^/s__/" >12S.species

echo "Combine all taxonomic name columns.."
paste -d " " 12S.class 12S.order 12S.family 12S.genus 12S.species | sed "s/.*f__Family.*$/Taxon/" >12S.taxon

echo "Merge feature ID and taxon information.."
paste -d "\t" 12S.featureID 12S.taxon >12S.taxonomy.tsv

echo "Import 12S sequences and taxonomies into QIIME2.."
qiime tools import --type 'FeatureData[Sequence]' --input-path mitofish.12S."$month".fasta --output-path 12S-seqs.qza
qiime tools import --type 'FeatureData[Taxonomy]' --input-path 12S.taxonomy.tsv --output-path 12S-tax.qza

echo "Remove sequences with >=5 ambiguous bases and homopolymers>=8bp long.."
qiime rescript cull-seqs --i-sequences 12S-seqs.qza --o-clean-sequences 12S-seqs-cleaned.qza

echo "Dereplicate cleaned sequences in uniq mode to retain identical sequence records with differing taxonomies.."
# Use vsearch bundled with qiime2 environment (V2.7.0). Do not use latest version of vsearch in bash profile
qiime rescript dereplicate --i-sequences 12S-seqs-cleaned.qza --i-taxa 12S-tax.qza --p-rank-handles 'silva' --p-mode 'uniq' --o-dereplicated-sequences 12S-seqs-derep-uniq.qza --o-dereplicated-taxa 12S-tax-derep-uniq.qza

echo "Export cleaned and dereplicated 12S data.."
qiime tools export --input-path 12S-seqs-derep-uniq.qza --output-path 12S.seq
qiime tools export --input-path 12S-tax-derep-uniq.qza --output-path 12S.tax

echo "Concatenate 12S+SILVA (16S & 18S) data.."
head -1 12S.tax/taxonomy.tsv >tax.header
cat 12S.tax/taxonomy.tsv silva138.99.tax/taxonomy.tsv | grep -v "Feature ID" >SSU.taxonomy
cat tax.header SSU.taxonomy >SSU.taxonomy.tsv
cat 12S.seq/dna-sequences.fasta silva138.99.seq/dna-sequences.fasta >SSU.fasta

echo "Import 12S+SILVA (16S & 18S) data into QIIME 2.."
qiime tools import --type 'FeatureData[Sequence]' --input-path SSU.fasta --output-path 12S-16S-18S-seqs.qza
qiime tools import --type 'FeatureData[Taxonomy]' --input-path SSU.taxonomy.tsv --output-path 12S-16S-18S-tax.qza
