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



folderpath=raw_input('Enter your folder path for patient to summarize:')
#print folderpath
subDir=[]
os.chdir(folderpath)
for subd in glob.glob("*/"):
    folders=folderpath + subd
    subDir.append(folders)
if len(subDir)==0:
    subDir.append(folderpath)
for foder in subDir:
    os.chdir(foder)
    print foder
    allsentTerm=[]
    docArr=[]
    docsentArr=[]
    Dcount=[]
    RawSarr=[]
    datef=[]
    totalConcept=[]
    sortdate=[]
    rSent=[]
    ############################################
    #   get concepts in all files as one
    ############################################
    allConcept=[]
    conArr=[]

    filect=0
    for files in glob.glob("*_cln.txt"):
        Rawdoc=open(files).read()
        print "filename", filect, ":",files
        docdat=[]
        splitRawdoc=[]
        splitRawdoc=Rawdoc.splitlines()
        for i in splitRawdoc:
            txt="Date seen:"
            if txt in i:
                y=i.index(":")
                de=re.sub('^\s*','',i[y+1:])
                #print "mydate", de
                docdat.append(str(filect))
                docdat.append(de)
                datef.append(docdat)
                break    
        docConcept= deffiles.preprocessing_step(Rawdoc)
        eachDocCon= sorted(set(docConcept))    #This is the concept in each file
        allConcept+=docConcept
        docsent=deffiles.procdoctosent(Rawdoc,filect)
        RawSarr+=[docsent]
        filect+=1
    tarsnt=RawSarr
    allDocConcept=sorted(set(allConcept))
    print "totalsentences", len(allDocConcept)
    #============================================================
    #   This gets the terms in each sentence of each file
    #============================================================
    for dc in xrange(0,len(RawSarr)):
        eachdocsent=[]
        for w in RawSarr[dc]:
            sentTerm=deffiles.preprocessing_step(w)
            allsentTerm.append(sentTerm)
            eachdocsent.append(sentTerm)
        docsentArr.append(eachdocsent)

    #===========================================================
    #   This gets the number of documents a term appears
    #===========================================================
    conFreq=[]
    for i in allDocConcept:
        Nsent=len([h for sublist in allsentTerm for h in set(sublist) if h==i])     #counts the number of sentences concept i appears
        conFreq.append(Nsent)
    totalvector=[]
    kie=0
    for mu in xrange(0,len(docsentArr)):
        for l in xrange(0,len(docsentArr[mu])):     #sentences as columns, concepts as rows
            m=docsentArr[mu][l]
            scode="D"+ str(mu)+ "S"+ str(l)##This keeps the original track of sentences in RawSarr
            sentvector=[]
            for j in allDocConcept:
                indy=allDocConcept.index(j)
                if j in m:
                    countg=m.count(j)      #counts frequency c in a sentence
                    Tf=countg/len(m)
                    idf= float(log(len(allsentTerm)/conFreq[indy]))
                    tf_idf=Tf*idf
                    if tf_idf==0:
                        print "idf is zero"
                    sentvector.append(tf_idf)
                else:
                    sentvector.append(0)
            if all([v==0 for v in sentvector])== True:
                tarsnt[mu][l]= ''
                kie+=1
            else:
                totalvector=totalvector+[sentvector]
                Dcount.append(scode) 
    tarsnt=[[x for x in tarsnt[s] if x]for s in range(len(tarsnt)) ]
    print  "Total Vectors after the TF -IDF" , len(totalvector), "zero concept = ",kie
        
    edgesmatrix=[]
    for m in range(len(totalvector)-1):
        #edgematrix=[]
        for n in range(m+1,len(totalvector)):
            edgematrix=[]
            simEdge=deffiles.cossimbtwsentences(totalvector[m],totalvector[n])
            if simEdge> 0.:
                edgematrix.append(m)
                edgematrix.append(n)
                edgematrix.append(simEdge)
                edgesmatrix=edgesmatrix+[edgematrix] 
    print len(edgesmatrix)
    #==============================================================
    # Adding weights to the edges and changing to undirected graph
    #===============================================================
    D=nx.DiGraph()
    for i in edgesmatrix:
        u=i[0]
        v=i[1]
        d=i[2]
        D.add_edge(u,v, weight=d)
    G= D.to_undirected()

    #================================================
    # Page rank calculation with max iterations
    #================================================
    nx.draw(G)
    #plt.show()
    ranking = nx.pagerank(G, max_iter=200)
    sortedrank=[]
    items=list(ranking.items())
    sortedrank=sorted(items,key=lambda x: x[1],reverse=True)
    swnoEdges=[]
    for i in xrange(0, len(totalvector)-1): ## There is no need
        if i not in [x[0] for x in items]:
            swnoEdges.append(Dcount[i])
    print "sentences with no edges ", swnoEdges, "length of ranked sentence ", len(sortedrank)
    addcode=[(Dcount[x[0]],x[1]) for x in sortedrank]
    rSent=[x[0] for x in addcode]
    originalrank=rSent
    #============================================================
    # Sortind Date on each file
    #============================================================
    sortdate=sorted(datef,key=lambda x: x[1])
    def getdocdate(docNo):
        for q in sortdate:
            if docNo == int(q[0]):
                dx=sortdate.index(q)
        return dx

    #============================================================
    # Checking for Redundancy in the summary
    #============================================================
    trf=0
    newsent=[]
    kipdel=[]
    for i in xrange(0,len(rSent) -1):
        if rSent[i]=="":
            continue
        (idocx,isnt)=callorder(rSent[i])
        sent1=docsentArr[idocx][isnt]
        ordi=getdocdate(idocx)
        for j in xrange(i+1,len(rSent)):
            if rSent[j]=="":
                continue
            (jdocx,jsnt)=callorder(rSent[j])
            sent2= docsentArr[jdocx][jsnt]
            redundantcheck=difflib.SequenceMatcher(None, sent1, sent2)
            redundantratio=redundantcheck.ratio()
            ordj=getdocdate(jdocx)
            #print "the redundancy ratio:", rSent[i], rSent[j]
            if (redundantratio >= 0.6):
                trf+=1
               # print "the same:", rSent[i], rSent[j], redundantratio
                if ordi >= ordj:
                    kipdel.append(rSent[j])
                    rSent[j]=""
                    continue
                else:
                    sent1=sent2
                    ordi=ordj
                    kipdel.append(rSent[i])
                    rSent[i]=rSent[j]
                    rSent[j]=""
                    continue
    rSent=[x for x in rSent if x]
    print "No of the same sentences ", trf, "rSEnt ", len(rSent)      
    kiptrk=0
    nName=os.path.basename(os.path.normpath(foder))
    fiame= nName+"_delenorm"
    fu=open(fiame, "w")
    for i in kipdel:
        (docx,snt)=callorder(i)
        sent=i +RawSarr[docx][snt]+ '\n'
        fu.write(sent)
    fu.close()
    mysumms=[]
    finame= nName+"_mysystem3.txt"
    fout = open(nName +"z.htm", "w")
    f=open(finame, "w")
    print >>fout,"""<title>sentence Ranking </title><html><head><h1>Sentence Ranking of %s</h1></head><body></br>""" %nName
    for i in rSent:
        (docx,snt)=callorder(i)
        kiptrk+=1
        sent=RawSarr[docx][snt]+ '\n'
        mysumms.append(sent)
        f.write(sent)
        print >>fout, "<table><tr>%s: %s</tr>"%(i,sent) 
        if kiptrk==100:
                break
    print >>fout, """</table></body></html>""" 
    fout.close()
    f.close()
     
