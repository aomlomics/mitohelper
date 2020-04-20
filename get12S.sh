[ $# -eq 0 ] && { echo "Usage: $0 <inputfile> <output_prefix>"; exit 1; }

[ ! -f $1 ] && { echo "Input file does not exist! Please try again! Exiting..."; exit 1; }
[ -z "$2" ] && { echo "Please specify an output file. Exiting..."; exit 1;}
[ -f $2_fulltaxonomy.hits* ] && { echo "Output file exists! Please rename output file. Exiting..."; exit 1; } 
[ -f $2_species.hits* ] && { echo "Output file exists! Please rename output file. Exiting..."; exit 1; } 
[ -f $2_genus.hits* ] && { echo "Output file exists! Please rename output file. Exiting..."; exit 1; } 


[ "$1" == "-h" ] && { echo "Usage: grep.sh <inputfile> <outputfile>"; exit 1; }

i=0

while IFS= read -r line
do
i=$((i+1))
fullcount=`grep -c "$line" 12S.list`
echo "=== Searching query #$i===="
fullcount=`grep -c "$line" 12S.list`
echo "$line hits (full taxonomy): $fullcount"
grep "$line" 12S.list >>$2_fulltaxonomy.hits

species=`echo $line | awk -F " " '{OFS=" "}{print $1,$2}'`
speciescount=`grep -c "$species" 12S.list`
echo "$species hits (species): $speciescount"
grep "$species" 12S.list >>$2_species.hits

genus=`echo $line | awk -F " " '{print $1}'`
genuscount=`grep -c "$genus" 12S.list`
echo "$genus hits (genus): $genuscount"
grep "$genus" 12S.list >>$2_genus.hits

done < $1

uniq $2_fulltaxonomy.hits >$2_fulltaxonomy.hits.txt 
uniq $2_species.hits >$2_species.hits.txt
uniq $2_genus.hits >$2_genus.hits.txt

rm $2_fulltaxonomy.hits
rm $2_species.hits
rm $2_genus.hits

echo "==== Run complete! ==="
echo "Accession number of full taxonomy hits and description saved in <$2_fulltaxonomy.hits.txt>" 
echo "Accession number of species hits and description saved in <$2_species.hits.txt>" 
echo "Accession number of genus hits and description saved in <$2_genus.hits.txt>" 
