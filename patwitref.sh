#!/bin/bash
dbname="rtfnotes"
username="tomodunbi"
for i in `cat 1_patdocid.txt`; do
j=`echo "$i" | cut  -d \| -f 1`
k=`echo $i | cut -d \| -f 2`
ka=`psql -A -t $dbname $username  -c "select count (*) from rtfnotes where patientid = $j and (notertf ~* 'Thank you for referring|referred to me');"`
echo $j $k
if [ $ka -gt 0 ]; then
test -d ./1_patnotes/$j || mkdir -p ./1_patnotes/"$j"
if ! [ -f 1_patnotes/$j/${j}_docids.txt ]; then
psql -A -t $dbname $username  -c "select documentid from rtfnotes n left join notetxt txt on txt.de_id = n.de_id where patientid = $j" > ./1_patnotes/$j/${j}_docids.txt
echo "$j"  >> ./1_patnotes/1_trackfiles.txt
fi
for c in `cat ./1_patnotes/$j/${j}_docids.txt`; do
if ! [ -f 1_patnotes/$j/${c}_recs.txt ]; then
psql -A -t $dbname $username  -c "select * from rtfnotes n left join notetxt txt on txt.de_id = n.de_id where documentid = $c" > ./1_patnotes/$j/${c}_recs.txt
fi
done
fi
done
