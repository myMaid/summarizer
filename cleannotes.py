from __future__ import division
import re
import glob
import os
import os.path
#import RTF

#===========================
# Opening of document
#===========================
folderpath = input('Enter your folder path:');
print(folderpath)
os.chdir(folderpath)
savePath='*************'
fileList=[]
for files in glob.glob("./*/*_recs.txt"):
     fileList.append(files)
for eachfile in fileList:
    newnotes=[]
#    print eachfile
    Nfile="".join((list(eachfile))[:-9]) + "_cln.txt"
    Rawdoc=open(eachfile).read()
    splitRawdoc=[s for s in re.split('[\|]',Rawdoc)]
    completeName = os.path.join(savePath, Nfile)
    print(completeName)
    if not os.path.exists(os.path.dirname(completeName)):
        os.makedirs(os.path.dirname(completeName))
    with open(completeName, "w") as f:
      f.write('Document ID: ' + splitRawdoc[2])
      f.write("\n Patient ID:  " + splitRawdoc[10])
      f.write("\nDocument Type: " +  splitRawdoc[3])
      f.write("\nDate seen:   " + splitRawdoc[9])
      f.write("\nSpecialty:  " + splitRawdoc[16])
      f.write("\nAuthor's ID: " + splitRawdoc[13]) 
      f.write("\n Notes: \n\n" + splitRawdoc[-1])
    f.close()
    #this stores all the concept in a list
#print "first concept",len(totalConcept)