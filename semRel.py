#!/home/tomodunbi/env/ python
#this extract all concepts in a file and keeps in a file
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
import glob
import os
import os.path
import sys
import shutil

folderpath=raw_input('Enter your folder path for patient to summarize:')
#print folderpath
savePath='******'
subDir=[]
os.chdir(folderpath)
filect=0
for subd in glob.glob("*/"):
    folders=folderpath + subd
    subDir.append(folders)
if len(subDir)==0:
    subDir.append(folderpath)
for foder in subDir:
    os.chdir(foder)
    #print foder
    ############################################
    #   get concepts in all files as one
    ############################################
    allConcept=[]
    conArr=[]
    for files in glob.glob("*_cln.txt"):
        fiame= savePath +os.path.basename(os.path.normpath(foder))+files[:-8]+".con"
        fu=open(fiame, "w")
        metamapfile=open(files + ".out").read()
        splitMetmap=metamapfile.splitlines()
        for c in splitMetmap:
            metSplit=[s for s in re.split('[\|]',c)]
            conmg=re.sub(' +', '_', metSplit[8]) + "\n"
            fu.write(conmg)
        filect+=1
        fu.close()
print "the total files process are: ", filect
