cleannotes.py file checks all files and resave it in a format that identifies each patient and visit. 
the formate extract patient id, date, doctor's id and main notes. 
all files of the patients are then put in a folder

clean.sh extract information from database. 
it counts the total files associated with patients and words before selecting the patient for processing

deffiles.py define functions to be used in the summarizer. it started with removing stopwords and stemming words using porterstemmer
then defining age groups to cosine similarity functions ansd ao on
text are changed to sentences for easy summary and meaningful result


Metamaptocsv.java is a modified code in UMLS server to semantically extract medical terms in patients’ files.
the CUI generated here are used to process the sentences


patwitref.sh is a linux code to extract patients that had at least one discharge summary so this can be used for evaluation.

redundancy.py is an implemented algprithm for elimination redundancy in the summary result

semrel.py is a code that keeps the list of concept of each file and label the file as .out
 

Semsumm.py is the full semmantic summarizer  packing files to use as input, use concepts generated, calculate tf-idf, 
get vector values, calculate cosine similarity  and add weight to the graph. 
page rank is calculated before redundancy is checked
result is printed and saved as summary of the patient clinical history

time exec calculates the time used to execute summarizer


normalmulti is a summarizer without the use of semantics. the purpose is to compare the ourput of semantic system with this.
 all other methods are applied


