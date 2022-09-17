#!/bin/bash
memap() {
 currFolder=$(pwd)
 if [ ! -f $currFolder/metamap_$1.log ]; then
  echo "creating new metamap log: $currFolder/metamap_$1.log"
  echo "metamap_logs" > $currFolder/metamap_$1.log
 fi;
 for i in "$2"/*;do
   if [ -d "$i" ];then
      echo "dir: $i";
      memap "$i";
   elif [ -f "$i" ]; then
     y="${i%/*}"
     echo "$i" | grep -qE ".txt$";
   if [[ $? -eq 0 ]]; then
     if [ ! -e $i.out ]; then
     tr -cd '\11\40-\176' < "$i" > $y/clean.txt;   #cat $currFolder/metamap_$2.log;
     java -cp "/opt/public_mm_linux_main_2014/src/javaapi/dist/prologbeans.jar:/opt/public_mm_linux_main_2014/src/javaapi/target/classes:." MetaMapToCSV $y/clean.txt config_file 8066 >"$i.out";
     fi;
     test=`find $i.out -type f|xargs grep -rli "no connection to Prolog Server\|Connection refused\|Connection reset\|java.io.IOException"|wc -l`;
     tr -cd '\11\40-\176' < "$i" > $y/clean.txt; 
     until [[ $test -eq 0 ]]; do
       echo $test “bad things happened”;  echo "$i:METAMAP_FAIL:$1" >> $currFolder/metamap_$1.log; sleep 10;
       rm $i.out;
       java -cp "/opt/public_mm_linux_main_2014/src/javaapi/dist/prologbeans.jar:/opt/public_mm_linux_main_2014/src/javaapi/target/classes:." MetaMapToCSV $y/clean.txt config_file 8066 >"$i.out";
       test=`find $i.out -type f|xargs grep -rli "no connection to Prolog Server\|Connection refused\|Connection reset\|java.io.IOException"|wc -l`;
     done;
       echo "$i:CLEAN_OK:$1" >> $currFolder/metamap_$1.log;
       echo "$i OK"; 
    fi;
   fi;
done; }


#this looks for file not yet processsed by metamap and the ones with errors
for i in `ls -d selected/2*`;do
   if [ -d "$i" ];then
     # echo "dir: $i";
      for k in `ls $i/*`; do
      if [ -f "$k" ]; then
        echo "$k" | grep -qE ".txt$";
        if [[ $? -eq 0 ]]; then
           if [ ! -e $k.out ]; then
               y="${k%/*}"
               tr -cd '\11\40-\176' < "$k" > $y/noclean.txt;
               java -cp "/opt/public_mm_linux_main_2014/src/javaapi/dist/prologbeans.jar:/opt/public_mm_linux_main_2014/src/javaapi/target/classes:." MetaMapToCSV $y/noclean.txt config_file 8066 >"$k.out";
               echo "$k:CLEAN_OK:" >> metamap_2.log;
             echo "$k:CLEAN_OK:"
           fi
               test=`find $k.out -type f|xargs grep -rli "no connection to Prolog Server\|Connection refused\|Connection reset\|java.io.IOException"|wc -l`;
               tr -cd '\11\40-\176' < "$k" > $y/noclean.txt;
               until [[ $test -eq 0 ]]; do
                  echo $test “bad things happened” $k; 
                  echo "$k:METAMAP_FAIL:" >> metamap_2.log;
                  sleep 10;
                  rm $k.out;
                  java -cp "/opt/public_mm_linux_main_2014/src/javaapi/dist/prologbeans.jar:/opt/public_mm_linux_main_2014/src/javaapi/target/classes:." MetaMapToCSV $y/noclean.txt config_file 8066 >"$k.out";
                  test=`find $k.out -type f|xargs grep -rli "no connection to Prolog Server\|Connection refused\|Connection reset\|java.io.IOException"|wc -l`;
               done 
             
        fi;
        fi;
     done;
      fi;
   done
   
   
   
   
   
#this checks for all files to see the ones with metamap errors
for i in `ls -d selected/*`;do
   if [ -d "$i" ];then
     # echo "dir: $i";
      for k in `ls $i/*`; do
        if [ -f "$k" ]; then
           if [ -f $k.out ]; then
               y="${k%/*}"
               test=`find $k.out -type f|xargs grep -rli "no connection to Prolog Server\|Connection refused\|Connection reset\|java.io.IOException"|wc -l`;
               until [[ $test -eq 0 ]]; do
                  echo $test “bad things happened” $k; 
                  rm $k.out;
                  tr -cd '\11\40-\176' < "$k" > $y/nuclean.txt;
                  java -cp "/opt/public_mm_linux_main_2014/src/javaapi/dist/prologbeans.jar:/opt/public_mm_linux_main_2014/src/javaapi/target/classes:." MetaMapToCSV $y/nuclean.txt config_file 8066 >"$k.out";
                  test=`find $k.out -type f|xargs grep -rli "no connection to Prolog Server\|Connection refused\|Connection reset\|java.io.IOException"|wc -l`;
                  if [[ $test -eq 0 ]];then
                   echo "$k:CLEAN_OK:" >> metamap_redo.log;
                   else
                   echo "$k:METAMAP_FAIL:" >> metamap_redo.log;
                   sleep 10;
                   fi;
             done 
           fi;
        fi;
     done;
   fi;
   done