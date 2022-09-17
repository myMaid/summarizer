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
fopen=open("/dxxxxxxxxxxxxxxxx/ConmtdErr.txt", "a")
fmet=open("/dxxxxxxxxxxxxxx/moreCon.txt", "a")
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
    allsentCon=[]
    docArr=[]
    docmemapArr=[]
    memapDoc=[]
    memapArr=[]
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
    refopen=open('referral.txt').read()
    reflen=len(refopen.split(" "))
        
    ############################################
    #   get concepts in all files as one
    ############################################
    allConcept=[]
    conArr=[]

    filect=0
    for files in glob.glob("*_cln.txt"):
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
        if de=="":
            entof="filename" + str(filect) + ":" + files +"No date" + "\n"
            fmet.write(entof)
        metamapfile=open(files + ".out").read()
        splitMetmap=metamapfile.splitlines()
        memapArr.append(splitMetmap)
        docConcept=[]
        #docSn="D" + str(ct) + ":"
        
        for c in splitMetmap:
            metSplit=[s for s in re.split('[\|]',c)]
            allConcept.append(metSplit[8])
            docConcept.append(metSplit[8])
        eachDocCon= sorted(set(docConcept))    #This is the concept in each file
        conArr.append(eachDocCon)
        docsent=deffiles.procdoctosent(Rawdoc,filect,foder,files,fopen)
        #text_file=tokenizer.tokenize(Rawdoc)
        RawSarr+=[docsent]
        filect+=1
    tarsnt=RawSarr
    allDocConcept=sorted(set(allConcept))
    #print "All bag concepts", len(conArr)

    #============================================================
    #   This getd the concepts in each sentence of each file
    #============================================================
    for dc in xrange(0,len(RawSarr)):
        #====================================
        # getting Concepts in each sentence
        #====================================
        #totalConcept=[]
        sentConcept=[]
        k=0
        #print "next doc ", dc
        for w in RawSarr[dc]:
            splitConcept=[]
            #nextIndex = k
            for m in list(memapArr[dc]):
                metSplit=[s for s in re.split('[\|]',m)]
                metSplit[1]=metSplit[1].rstrip('\.')
                if re.sub('\s+',' ',metSplit[1]) in w:
                    splitConcept.append(metSplit[8])
                    memapArr[dc].remove(m)
            sentConcept=sentConcept + [splitConcept]
            allsentCon.append(splitConcept)
        if len(memapArr[dc])>10:
            newmsg=  "D"+ str(dc)+" remaining " + str(len(memapArr[dc]))
            fmet.write(newmsg)
        docmemapArr.append(sentConcept)

    #===========================================================
    #   This gets the number of documents a concept appears
    #===========================================================
    conFreq=[]
    for i in allDocConcept:
        Nsent=len([h for sublist in allsentCon for h in set(sublist) if h==i])     #counts the number of sentences concept i appears
        conFreq.append(Nsent)
    totalvector=[]
    kie=0
    for mu in xrange(0,len(docmemapArr)):
    #    eachitem=[("D"+ str(filect)+ "S"+ str(x[0]), x[1]) for x in items]
        
        for l in xrange(0,len(docmemapArr[mu])):     #sentences as columns, concepts as rows
            m=docmemapArr[mu][l]
            scode="D"+ str(mu)+ "S"+ str(l)##This keeps the original track of sentences in RawSarr
            #Dcount.append(scode)
            sentvector=[]
            for j in allDocConcept:
                indy=allDocConcept.index(j)
                if j in m:
                    countg=m.count(j)      #counts frequency c in a sentence
                    Tf=countg/len(m)
                    idf= float(log(len(allsentCon)/conFreq[indy]))
                    tf_idf=Tf*idf
                    if tf_idf==0:
                        print "idf is zero"
                    sentvector.append(tf_idf)
                else:
                    sentvector.append(0)
            #print "sent vector ", len(sentvector), sentvector
            if all([v==0 for v in sentvector])== True:
                #print "no concept"
                tarsnt[mu][l]= ''
                kie+=1
            else:
                totalvector=totalvector+[sentvector]
                Dcount.append(scode) 

    tarsnt=[[x for x in tarsnt[s] if x]for s in range(len(tarsnt)) ]
    #print  "Total Vectors after the TF -IDF" , len(totalvector), "zero concept = ",kie
        
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
    #print len(edgesmatrix)

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
    #swnoEdges=[]
    #for i in xrange(0, len(totalvector)-1): ## There is no need
    #    if i not in [x[0] for x in items]:
    #        swnoEdges.append(Dcount[i])
    #print "sentences with no edges ", swnoEdges, "length of ranked sentence ", len(sortedrank)
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



    #============================================================
    # Checking for Redundancy in the summary
    #============================================================
    secsumm=rSent[:]
    trf=0
    newsent=[]
    kipdel=[]
    for i in xrange(0,len(rSent) -1):
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
            sent1= sorted(set(preprocessing_step(firstpair)))
            sent2= sorted(set(preprocessing_step(secondpair)))
            if all(x in sent1 for x in sent2)== True:
                ordi=ordj
                print "sent 2 more", rSent[i], rSent[j]
                kipdel.append(rSent[i])
                rSent[i]=rSent[j]
                rSent[j]=""
                continue
            elif all(x in sent2 for x in sent1)== True:
                print "sent1 more", rSent[i], rSent[j]
                kipdel.append(rSent[j])
                rSent[j]=""
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
                        continue
                    else:
                        ordi=ordj
                        kipdel.append(rSent[i])
                        rSent[i]=rSent[j]
                        rSent[j]=""
    rSent=[x for x in rSent if x]
    #print "No of the same sentences ", trf, "rSEnt ", len(rSent)      

    #============================================================
    # Printing the summary
    #============================================================
##################################################
#   Get some sentences as first set of sentences
##################################################
    finalsumm=[]
    mysumms=[]
    kiptrk=0
    nName=os.path.basename(os.path.normpath(foder))
    fiame= nName+"_delec"
    fu=open(fiame, "w")
    for i in kipdel:
        (docx,snt)=callorder(i)
        sent=i +RawSarr[docx][snt]+ '\n'
        fu.write(sent)
    fu.close()
    finame= nName+"concept.txt"
    fiabst=nName+"abst.txt"
    fout = open(nName +"c.htm", "w")
    f=open(finame, "w")
#==============================================================
    fabst=open(fiabst,"w")
    q=int(sortdate[0][0])
    for j in RawSarr[q]:
        m=re.search(r"(dob|date\s+of\s+birth)",j.lower())
        n=re.search(r"(\s*\d+\s+y\.*o\.*|\s*\d+\s+year\w+old)"
        if m is not None:
            txt=m.group()
            y=j.index(":")
            patientbirth=re.sub('^\s*','',j[y+1:y+10])
            DOB=format_date(patientbirth)
            break
        
        elif n is not None:
            arryr= re.findall('\d+', ptt.group())       
            yr=int(arryr[0])
            dd=datetime.strptime(sortdate[q][1],'%Y-%m-%d %H:%M:%S')
            dd.year
            DOB='01/01/
    for j in RawSarr[q]:
        if re.search(r"(assessment|boy|girl|woman|lady|male|female|man|\s*\d+\s+y\.*o\.*|\s*\d+\s+year|dob|date\s+of\s+birth)",j.lower()) is not None:
            j
    today = date.today()
    currage=calculate_age(DOB,today)
    sent="patient ID:" + str(nName) +"DOB: "+str(DOB) +"(" + years"\n"
    fabst.write(sent)
    sent="A "+ gend +agerange+ " was first seen on " + sortdate[0][1] + " at age " + str(thatage) +"\n"
    fabst.write(sent)
    
    
    print >>fout,"""<title>sentence Ranking </title><html><head><h1>Sentence Ranking of %s</h1></head><body></br>""" %nName
    for i in rSent:
        (docx,snt)=deffiles.callorder(i)
        kiptrk+=1
        sent=RawSarr[docx][snt]+ '\n'
        #wordcount+=len(sent.split(" "))
        mysumms.append(sent)
        f.write(sent)
        print >>fout, "<table><tr>%s: %s</tr>"%(i,sent) 
        if kiptrk==100:
                break
    print >>fout, """</table></body></html>""" 
    fout.close()
    f.close()
    fmet.close()
    fopen.close()
