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





porter = nltk.PorterStemmer()
pattern=r'[^a-z0-9]'
stopwords = nltk.corpus.stopwords.words('english')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
def stem(word):
     regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$'
     stem, suffix = re.findall(regexp, word)[0]
     return stem

def callorder(meu):
    docx=int(meu[1:meu.index('S')])
    snt=int(meu[meu.index('S')+1:])
    return (docx,snt)

def preprocessing_step(rawdoc):
     dupliwordlower=rawdoc.lower()
     tokdupliword=nltk.wordpunct_tokenize(dupliwordlower)
     tokdupliword=[w for w in tokdupliword if w.lower() not in stopwords]
     stemmwords=[]
     for t in tokdupliword:
        #   t=t.decode('utf-8')
         try:
             stemmwords.append(porter.stem(t))
         except UnicodeDecodeError:
             stemmwords.append(t)
             #print "error text", t,dcode
             #stemmwords=[porter.stem(t) for t in tokdupliword]
             continue
     for w in stemmwords[:]:
          if re.search(pattern,w):
               stemmwords.remove(w)
     #print stemmwords
     return stemmwords


    #================================================
    # Categorise patient age to age group
    #================================================
def calculate_age(dob):
    today = date.today()
    years = today.year - dob.year
    try:
        birthday=datetime.date(today.year,dob.month,dob.day)
    except ValueError as e:
        if dob.month == 2 and dob.day == 29:
            birthday= datetime.date(dob.year, 2, 28)
        else:
            raise e
    if today < birthday:
        years -= 1
    return years
#print (calculate_age(birth))
#patientAge= input ('how old are you: ')
def ageGroup(patAge):
    if patAge < 0.07:
        ageGrp='Neonate'
    elif patAge >=0.07 and patAge < 1:
        ageGrp='Infant'
    elif patAge >=1 and patAge < 5:
        ageGrp='preschool'
    elif patAge >=5 and patAge < 11:
        ageGrp='schoolchild'
    elif patAge >=12 and patAge < 18:
        ageGrp='Adolescent'
    elif patAge >=18 and patAge < 45:
        ageGrp='young adult'
    elif patAge >=45 and patAge < 60:
        ageGrp='middle age'
    elif patAge >=60 and patAge < 75:
        ageGrp='adult'
    elif patAge >=75 and patAge < 90:
        ageGrp='elderly'
    elif patAge >=90 and patAge < 120:
        ageGrp='aged'
    else:
        print('Not a valid age')
    return ageGrp

    #================================================
    # Cosine similarity Calculation between sentences
    #================================================
def cossimbtwsentences(u,v):    #i need to pair#####
    cosresult=(dot(u,v)/(norm(u)*norm(v)))  #+  0.0000000000001
    if math.isnan(float(cosresult)):
         print "still nan?"
    return cosresult



def procdoctosent(docfile,Num,foder, filename,ferr):
    text_file=tokenizer.tokenize(docfile)
    #print "D" + str(Num)+ ": NLTK sentence token: " , len(text_file), "sentences"
    ##########################################
    #   Merging numbered List
    ##########################################
  
    for i in text_file:
         m= re.search(r"(^\d+\.$|^\d+\)$)" , i, re.MULTILINE)
         num=text_file.index(i)
         if m is not None: #for numberedlist starting newline but pick as end of sentence
             j=len(i)-len(m.group())
             text_file[num+1]= m.group() + text_file[num+1]
             i=i[:j]
             text_file[num]=i
    
    text_file=[x for x in text_file if x]
    #print "D" + str(Num)+ ": merge list: " , len(text_file), "sentences"
    ##Merging bullets as sentences under subtopic
    bullet=[]
    iListIndex=[]
    delSent=[]
    #print "before", len(mysent)
    for i in text_file:  #list is used so that one can remove the sentence already merged
         m= re.search(r"(^\d+\.|^\d+\))", i, re.MULTILINE) #check for sentences starting with a number
         num=text_file.index(i)
         if m is not None:
             gi=m.group()
             curList= float(gi[:-1])      #this stores the number and point
             iListIndex.append(num)
             if len(bullet)>0:
                 lastList= float(bullet[-1])
                 #print"last" ,lastList
             else:
                 lastList=0
             bullet.append(curList)    #keeps number in an array
             if (text_file[num-1].endswith(":"))or (curList==1.0):   #checks if the previous sentence ends with :
                 i=i[len(m.group()):]
                 text_file[num]=i
                 lastMerge=num
             elif (curList == lastList + 1):    #checks if the list is continuous
                 i=i[len(m.group()):]
                 text_file[num]=i
                 try:
                    text_file[lastMerge]=text_file[lastMerge] + "; " + i
                    delSent.append(num)
                 except UnboundLocalError:
                    texttt= "merge sentence error: D" + str(Num)+ " "+foder+"/"+ filename +"\n"
                    ferr.write(texttt)
                    continue 
                 
    delSent=list(set(delSent))  #removes duplicate indexes
    text_file=[x for x in text_file if text_file.index(x) not in delSent]
    text_file=[x for x in text_file if x]
    #print "D" + str(Num)+ ": more merge list: " , len(text_file) , "sentences"
    #############################################
    ###more sentence breaking
    #############################################
    mysent=[]
    for i in text_file:
         n= re.search(":", i, re.MULTILINE)
         num=text_file.index(i)
         numis=len(mysent)
         position=[]
         if n is not None: #for subtopics that ends a line
              targetChar=set("\n")
              position = [index for index, char in enumerate(i) if char in targetChar]
              if i[0] !="\n":
                   position.insert(0,0)
                   lasti=numis
              for ind in position:
                   g=position.index(ind)
                   if g < len(position)-1:
                        y=i[position[g]:position[g+1]]
                   else:
                        y=i[position[g]:]
                   if ":" in y and (y.endswith(":") or y[y.index(":")+1].isspace()):
                        mysent.append(y)
                   else:
                        lasti=len(mysent)
                        if lasti!=numis:
                             mysent[lasti-1]= mysent[lasti-1] + y
                        else:
                             mysent.append(y)
         else:
              mysent.append(i)
     
    for x in mysent:
         num=mysent.index(x)
         p= re.sub('\|+','',x)
         x=re.sub('\s+',' ',p)
         mysent[num]=x
         num=mysent.index(x)
         if num>0 and x[0].islower():
              c= re.search("\w\.\w\.$", mysent[num-1])
              if c is not None:
                   mysent[num-1]= mysent[num-1] + ' ' + x
                   mysent[num]=""
    mysent=[x for x in mysent if x] 
    for m in list(mysent[:-1]):
         if m=="":
              continue
         indy= mysent.index(m)
         x=mysent[indy-1]
         if (x.endswith(".")or x.endswith(",")) and (m[0].islower() or re.match("^[\.,;:]", m)):
              mysent[indy]= x + ' ' + mysent[indy]
              mysent[indy-1]=""
    mysent=[x for x in mysent if x]
    #print "D" + str(Num)+ ": more sentence analysis: " , len(mysent), "sentences"
    return mysent
