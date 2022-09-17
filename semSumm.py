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



folderpath=raw_input('Enter your folder path for patient to summarize:')
#print folderpath
ftermv=open("/xxxxxxxxx/termvectors2.txt").read()#"/xxxxxxxxxxxxxx/ConmtdErr.txt", "a")
fmet=open("/hxxxxxxxx/Vectcon.txt", "a")#"/xxxxxxxxxxx/moreCon.txt", "a")
fs=open("/xxxxxxxxxxxx/fileSuccess.txt", "a")#"/xxxxxxxxxxx/fileSuccess.txt", "a")
termv=ftermv.splitlines()
vetc=[]
getcon=[]
for c in xrange(0,len(termv)):
    gettc=termv[c].split("|")
    getcon.append(gettc)
    vetc.append(gettc[0])
#print "vector total", len(getcon)
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
    nName=os.path.basename(os.path.normpath(foder))
    finame= nName+"_semvec.txt"
##    if os.path.isfile(finame)==True:
##        continue
    print foder
    allsentCon=[]
    docArr=[]
    Dcount=[]
    RawSarr=[]
    datef=[]
    dConcept=[]
    conLen=[]
    totalConcept=[]
    allFileConcept=[]
    pilerank=[]
    joinRfiles=[]
    sortdate=[]
    rSent=[]
      ############################################
    #   get concepts in all files as one
    ############################################
    allConcept=[]
    filect=0
    for files in glob.glob("*_sp.txt"):
        Rawdoc=open(files).read()
        #print "filename", filect, ":",files
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
            else:   #there is no way you wont find a date so remove this
                de=""
        
        fmm=open(files[:-4] + "c.txt").read()
        fMetmap=fmm.splitlines()
        RawSarr+=[splitRawdoc]
        allFileConcept+=[fMetmap]
        filect+=1
    tarsnt=RawSarr
    allDocConcept=open(nName+ "_allcon.txt").read().split('\n')
    allDocConcept=[x for x in allDocConcept if x]
    Asconcepts=open(nName+"conAsent.txt").read()
    sentCons=Asconcepts.splitlines()
    allsentCon=[]
    for p in sentCons:
        ser=p.split("|")
        if len(ser)>1:
            ser=ser[:-1]
        allsentCon.append(ser)
         
    #============================================================
    #   This get the concepts in each sentence of each file
    #============================================================
    conFreq=[]    
    for i in allDocConcept:
        Nsent=len([h for sublist in allsentCon for h in set(sublist) if h==i])     #counts the number of sentences concept i appears
        conFreq.append(Nsent)
    kie=0
    fct=0
    foldercon=[]
    allsent=[]
    docidf=[]
    for doc in allFileConcept:
        ct=0
        sentarr=[]
        for st in doc:
            scode="D"+ str(fct)+ "S"+ str(ct)##This keeps the original track of sentences in each file
            senttfidf=[]
            wd=st
            wd=st.split("|")
            if len(wd)>1:
                wd=wd[:-1]
                st=wd[:-1]
            sentarr.append(wd)
            allsent.append(wd)
            if st=='':
                ct+=1
                continue
            for l in wd:
                indy=allDocConcept.index(l)        
                countg=wd.count(l)      #counts frequency c in a sentence
                Tf=countg/len(wd)
                idf= float(log(len(allsentCon)/conFreq[indy]))
                tf_idf=Tf*idf
                if tf_idf==0:
                    print "idf is zero"
                senttfidf.append(tf_idf)
            docidf.append(senttfidf)
            Dcount.append(scode)
            ct+=1
        foldercon+=[sentarr] #pack sent concepts with empty concept in each file
        fct+=1
    print "Ist", len(Dcount)
    #============================================================================================
    #   get the vetor values by multiplying the tfidf with semantic vector value and adding them
    #=============================================================================================
    arrdim=int(termv[0][-4:]) #this gives a 3 difit dimensional array
    totalvector=[]
    tsv=[]
    kiprm=[]
    for o in xrange(0,len(docidf)):
        svt=[0]*arrdim
        (doct,sntx)=callorder(Dcount[o])
        sc=foldercon[doct][sntx]
        contfidf=docidf[o]
        for p in xrange(0,len(sc)):
            if sc[p]==['']:
                continue
            if sc[p] in vetc:
                q=vetc.index(sc[p])
                cvt=getcon[q][1:]
                sve=[float(x)*contfidf[p] for x in cvt]
                svt=map(add, svt,sve)
            else:
                fmet.write(sc[p])
##                vit=sc[p].split("_")
##                for r in vetc:
##                    if vit[0] in r:
##                        q=vetc.index(r)
##                        break
                
        if all([v==0 for v in svt])== True:
                print "no concept?"
        else:
            totalvector.append(svt)
            kiprm.append(o)
    #delSent=list(set(delSent))  #removes duplicate indexes
    Dcount=[x for x in Dcount if Dcount.index(x) in kiprm]        
    print "2nd", len(Dcount)
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
    # Stemming words in select sentences for redundancy
    #============================================================
    stemm=[]
    for i in xrange(0,len(rSent)):
        (docx,snt)=callorder(rSent[i])
        pai=RawSarr[docx][snt]
        stemm.append (sorted(set(preprocessing_step(pai))))
    #============================================================
    # Checking for Redundancy in the summary
    #============================================================
    secsumm=rSent[:]
    trf=0
    newsent=[]
    kipdel=[]
    for i in xrange(0,len(rSent)):
        if rSent[i]=="":
            continue
        (idocx,isnt)=callorder(rSent[i])
        secondpair=[]
        firstpair=[]
        firstpair=RawSarr[idocx][isnt] #mysumms[i]
        ordi=getdocdate(idocx)
        for j in xrange(i+1,len(rSent)):
            if rSent[j]=="":
                continue
            (jdocx,jsnt)=callorder(rSent[j])
            secondpair=RawSarr[jdocx][jsnt]
            ordj=getdocdate(jdocx)
            sent1= stemm[i]#sorted(set(preprocessing_step(firstpair)))
            sent2= stemm[j]#sorted(set(preprocessing_step(secondpair)))
            if all(x in sent1 for x in sent2)== True:
                ordi=ordj
                print "sent 2 more", rSent[i], rSent[j]
                kipdel.append(rSent[i])
                rSent[i]=rSent[j]
                rSent[j]=""
                stemm[j]=""
                continue
            elif all(x in sent2 for x in sent1)== True:
                print "sent1 more", rSent[i], rSent[j]
                kipdel.append(rSent[j])
                rSent[j]=""
                stemm[j]=""
                continue
            else:    
                redundantcheck=difflib.SequenceMatcher(None, sent1, sent2)
                redundantratio=redundantcheck.ratio()
                
                if (redundantratio >= 0.6):
                    trf+=1
                    #print "the same:", rSent[i], rSent[j], redundantratio
                    if ordi >= ordj:
                        kipdel.append(rSent[j])
                        rSent[j]=""
                        stemm[j]=""
                        continue
                    else:
                        ordi=ordj
                        kipdel.append(rSent[i])
                        rSent[i]=rSent[j]
                        stemm[i]=stemm[j]
                        rSent[j]=""
                        stemm[j]=""
    rSent=[x for x in rSent if x]
    print "No of the same sentences ", trf, "rSEnt ", len(rSent)      

    #============================================================
    # Printing the summary
    #============================================================
    finalsumm=[]
    mysumms=[]
    kiptrk=0
    f=open(finame, "w")
    for i in rSent:
        (docx,snt)=deffiles.callorder(i)
        kiptrk+=1
        sent=RawSarr[docx][snt]+ '\n'
        #wordcount+=len(sent.split(" "))
        mysumms.append(sent)
        f.write(sent)
        
        if kiptrk==100:
                break
    
    f.close()
fmet.close()
fs.close()
    

sys.exit()
    
