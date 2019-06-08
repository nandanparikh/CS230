
JARFOLDER=$1
CALLGRAPH=$2
mkdir $CALLGRAPH

cd $1

for f in *.jar; do 
     java -jar ../javacg-0.1-SNAPSHOT-static.jar $f > $2/${f%.jar}.txt
done
