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

fopen=open("/xxxxxxxxxxxxx/ConmtdErr.txt", "a")#"/dxxxxxxxxxx/ConmtdErr.txt", "a")
#below code stores the concept for semantic vector
fmet=open("/xxxxxxxxxxxxxxxxx/totVectcon.txt", "w")#"/xxxxxxxxxxxxxxxxxxxx/moreCon.txt", "a")
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
    savePath='/xxxxxxxxxxxxxx/sentparts/'+ nName+'/'#'/xxxxxxxxxxxxx/conRel/'+ nName+'/'    
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
    #fs=open(completesentcon, "w")
    filect=0
    for files in glob.glob("*_cln.txt"):
        Rawdoc=open(files).read()
        fiame= files[:-8]+"_sp.txt"
        completeName = os.path.join(savePath, fiame)
        fu=open(completeName, "w")
        docsent=deffiles.procdoctosent(Rawdoc,filect,foder,files,fopen)
        for w in docsent:
            fu.write(w + "\n" )
            splitConcept=""
        filect+=1
        fu.close()
fopen.close()
fmet.close()
