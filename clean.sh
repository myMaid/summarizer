#!/bin/bash
dbname="rtfnotes"
username="******"
for i in `cat fewerpatdocid.txt`; do
j=`echo "$i" | cut  -d \| -f 1`
k=`echo $i | cut -d \| -f 2`
test -d ./fewnotes/$j || mkdir -p ./fewnotes/"$j"
if ! [ -f fewnotes/$j/${j}_docids.txt ]; then
psql -A -t $dbname $username  -c "select documentid from rtfnotes n left join notetxt txt on txt.de_id = n.de_id where patientid = $j" > ./fewnotes/$j/${j}_docids.txt
fi
for c in `cat ./fewnotes/$j/${j}_docids.txt`; do
if ! [ -f fewnotes/$j/${c}_recs.txt ]; then
psql -A -t $dbname $username  -c "select * from rtfnotes n left join notetxt txt on txt.de_id = n.de_id where documentid = $c" > ./fewnotes/$j/${c}_recs.txt
fi
done
echo "patient " $j "finished running" >> trackfiles.txt
done
