[ $# -eq 0 ] && { echo "Usage: $0 <inputfile> <output_prefix> <12S.ref.tsv or mitofish.ref.tsv>"; exit 1; }

[ ! -f $1 ] && { echo "Input file does not exist! Please try again! Exiting..."; exit 1; }
[ -z "$2" ] && { echo "Please specify an output file. Exiting..."; exit 1;}
[ -z "$3" ] && { echo "Please specify a reference file (12S.ref.tsv or mitofish.ref.tsv). Exiting..."; exit 1;}
[ ! -f $3 ] && { echo "Reference file does not exist! Please try again! Exiting..."; exit 1; }

[ -f $2_subspecies* ] && { echo "Output file exists! Please rename output file. Exiting..."; exit 1; } 
[ -f $2_species* ] && { echo "Output file exists! Please rename output file. Exiting..."; exit 1; } 
[ -f $2_genus* ] && { echo "Output file exists! Please rename output file. Exiting..."; exit 1; } 


[ "$1" == "-h" ] && { echo "Usage: grep.sh <inputfile> <outputfile> <12S.ref.tsv or mitofish.ref.tsv>"; exit 1; }

i=0

while IFS= read -r line
do
i=$((i+1))

species=`echo $line | awk -F " " '{OFS=" "}{print $1,$2}'`
genus=`echo $line | awk -F " " '{print $1}'`

echo "=== Searching query #$i===="

if [ "$line" = "$genus" ]; then
genuscount=`grep -c "$genus" $3`
echo -e "Query:$genus\tLevel:genus\t# Hits: $genuscount"
grep "$genus" $3 >>$2_genus.hits
fi

if [ "$line" = "$species" ]; then
speciescount=`grep -c "$species" $3`
echo -e "Query:$species\tLevel:species\t# Hits: $speciescount"
grep "$species" $3 >>$2_species.hits

genuscount=`grep -c "$genus" $3`
echo -e "Query:$genus\tLevel:genus\t# Hits: $genuscount"
grep "$genus" $3 >>$2_genus.hits
fi

if [ "$line" != "$genus" ] && [ "$line" != "$species" ]; then
subcount=`grep -c "$line" $3`
echo -e "Query:$line\tLevel:subspecies\t# Hits: $subcount"
grep "$line" $3 >>$2_subspecies.hits

speciescount=`grep -c "$species" $3`
echo -e "Query:$species\tLevel:species\t# Hits: $speciescount"
grep "$species" $3 >>$2_species.hits

genuscount=`grep -c "$genus" $3`
echo -e "Query:$genus\tLevel:genus\t# Hits: $genuscount"
grep "$genus" $3 >>$2_genus.hits
fi

done < $1

echo "==== Run complete! ==="
 
# Check and report on the types of output files generated

[ ! -f $2_genus.hits ] && { echo "No genus detected in input file."; } 

if [ -f $2_genus.hits ]; then
awk '!seen[$0]++' $2_genus.hits >$2_genus.hits.txt
cat $2_genus.hits.txt | awk -F "\t" '{print $2}' | awk -F " " '{print $1}' | sed "s/$/\tgenus/g" >$2_genus.hits.left
paste -d "\t" $2_genus.hits.left $2_genus.hits.txt >$2_genus.hits.tsv
echo "Accession number of genus hits and description saved in $2_genus.hits.tsv" 
fi

[ ! -f $2_species.hits ] && { echo "No species detected in input file."; } 

if [ -f $2_species.hits ]; then
awk '!seen[$0]++' $2_species.hits >$2_species.hits.txt
cat $2_species.hits.txt | awk -F "\t" '{print $2}' | awk -F " " '{OFS=" "}{print $1,$2}' | sed "s/$/\tspecies/g" >$2_species.hits.left
paste -d "\t" $2_species.hits.left $2_species.hits.txt >$2_species.hits.tsv
echo "Accession number of genus hits and description saved in $2_species.hits.tsv" 
fi

[ ! -f $2_subspecies.hits* ] && { echo "No subspecies detected in input file."; } 

if [ -f $2_subspecies.hits ]; then
awk '!seen[$0]++' $2_subspecies.hits.txt >$2_subspecies.hits.txt
cat $2_subspecies.hits.txt | awk -F "\t" '{print $2}' | awk -F " " '{OFS=" "}{print $1,$2,$3}' | sed "s/$/\tsubspecies/g" >$2_subspecies.hits.left
paste -d "\t" $2_subspecies.hits.left $2_subspecies.hits.txt >$2_subspecies.hits.tsv
echo "Accession number of genus hits and description saved in $2_subspecies.hits.tsv" 
fi

rm $2_*hits.txt $2_*hits.left


