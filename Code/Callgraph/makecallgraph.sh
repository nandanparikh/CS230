for f in *.jar; do 
     java -jar javacg-0.1-SNAPSHOT-static.jar "$f" > "${f%.jar}.txt"
done
