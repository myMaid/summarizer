#!/home/tomodunbi/env/ python
from __future__ import division
import nltk, re, pprint
import math
import networkx as nx
import numpy
from numpy import *
from numpy.linalg import *
import numpy as np
import difflib
from nltk.corpus import stopwords #this imports all puntuations in nltk library
import random
from urllib import urlopen
import urllib
import matplotlib.pyplot as plt
import glob
import os
import os.path
import sys
import shutil
import datetime
from datetime import *
import deffiles
from deffiles import *



folderpath=raw_input('Enter your folder path for patient to clean:')
#print folderpath

fopen=open("/home/tessydunbi/data/test2/ConmtdErr.txt", "a")#"/data/tomodunbi/MedNotes/bukkienotes20150306/ConmtdErr.txt", "a")
#below code stores the concept for semantic vector
fmet=open("/home/tessydunbi/data/test2/totVectcon.txt", "w")#"/data/tomodunbi/MedNotes/bukkienotes20150306/moreCon.txt", "a")
subDir=[]
os.chdir(folderpath)
for subd in glob.glob("*/"):
    folders=os.path.normpath(folderpath)+"/" + subd
    subDir.append(folders)
if len(subDir)==0:
    subDir.append(folderpath)
for foder in subDir:
    if os.path.isdir(foder)==False:
        continue
    os.chdir(foder)
    print foder
    nName=os.path.basename(os.path.normpath(foder))
    savePath='/home/tessydunbi/data/sentparts/'+ nName+'/'#'/data/tomodunbi/MedNotes/bukkienotes20150306/conRel/'+ nName+'/'    
    allsentCon=[]
    docArr=[]
    Dcount=[]    
        
    ############################################
    #   get concepts in all files as one
    ############################################
    allConcept=[]
    conArr=[]
    completesentcon = os.path.join(savePath, nName+"conAsent.txt")
    if not os.path.exists(os.path.dirname(completesentcon)):
            os.makedirs(os.path.dirname(completesentcon))
    fs=open(completesentcon, "w")
    filect=0
    for files in glob.glob("*_cln.txt"):
        Rawdoc=open(files).read()
        metamapfile=open(files + ".out").read()
        splitMetmap=metamapfile.splitlines()
        fiame= files[:-8]+"_sp.txt"
        fcon= files[:-8]+"_spc.txt"
        completeName = os.path.join(savePath, fiame)
        completeNames = os.path.join(savePath, fcon)
        fu=open(completeName, "w")
        fc=open(completeNames, "w")
        docsent=deffiles.procdoctosent(Rawdoc,filect,foder,files,fopen)
        #text_file=tokenizer.tokenize(Rawdoc)
        for w in docsent:
            fu.write(w + "\n" )
            splitConcept=""
            for m in list(splitMetmap):
                metSplit=[s for s in re.split('[\|]',m)]
                metSplit[1]=metSplit[1].rstrip('\.')
                if re.sub('\s+',' ',metSplit[1]) in w:
                    ##change this back because of other systems
                    conmg=re.sub(' +', '_', metSplit[8] )
                    splitConcept+= conmg+"|"
                    allConcept.append(conmg)
                    splitMetmap.remove(m)
                    fmet.write("%s\n" % conmg )

            fc.write("%s\n" % splitConcept)
            #sentConcept=sentConcept + [splitConcept]
            if len(splitMetmap)>0:
                for i in splitMetmap:
                    metSplit=[s for s in re.split('[\|]',i)]
                    conmg=re.sub(' +', '_', metSplit[8] )
                    allConcept.append(conmg)
                    fmet.write("%s\n" % conmg )
            fs.write("%s\n" % splitConcept ) 
            allsentCon.append(allConcept)
        filect+=1
        fu.close()
        fc.close()
    fs.close()
    allconfile = os.path.join(savePath, nName+"_allcon.txt")
    thefile = open(allconfile, 'w')
    allDocConcept=sorted(set(allConcept))
    for ss in allDocConcept:
        print>>thefile, ss
    thefile.close()
    #print "All bag concepts", len(conArr)
    
    
fopen.close()
fmet.close()
