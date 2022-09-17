
library(RPostgreSQL)
library(sqldf)
library(tm)
####
####  data to match: 
####  /data/smalec/alchemy/code/sunnynotes/notes20130130MedLee00

# INSTRUCTIONS OF USAGE: 
# Rscript gn.R 3383809
# where  3383809 is documentid from rtfnotes in notes20130430 schema on BA Server

args <- commandArgs(trailingOnly = TRUE)
print(args)

documentid <- tolower(as.character(args[1]))

setwd("/data/smalec/alchemy/data/clinicalnotes.cleaned.txt")
drv = dbDriver("PostgreSQL")
con = dbConnect(drv, dbname='rtfnotes')
nrows = fetch(dbSendQuery(con, 'SELECT COUNT(*) FROM notes20140430.rtfnotes'))

nrows = fetch(dbSendQuery(con, 'SELECT COUNT(*) FROM notes20140430.notetxt'))

nr = as.numeric(nrows)
print(nr)
 # for (i in 1390156:nr) {
     query = paste('SELECT nt.notetxt FROM notes20140430.rtfnotes rn, notes20140430.notetxt nt WHERE rn.de_id = nt.de_id AND documentid = ', documentid, ' LIMIT 100;')
     # documenttype
       # de_id
       # mrn = medical record # mp_uid > mrn (get latest? - ask Chuck on Monday)
       #  ... specialty, encounterdate 
       data = as.data.frame(dbGetQuery(con, query))
 #    filename = paste(as.character(i), ".txt")
 #    filename = sub('[[:space:]]{1}', '', filename)
     if (length(data) > 0) { 
   #      write(t(data), file=filename)
          print("##################################")
    #      print(i)
          print("##################################")
          print(data) 
          print("##################################")
#         filename = paste(data[4], "_", as.character(as.Date(data[[10]])), ".txt", sep="")
#         filename = sub('[[:space:]]{1}', '', filename)
#         write(data[22], file=filename)
#         print(data[22])
       }
 # }

#data[4] # documenttype
#as.character(as.Date(data[[10]])) # encounterdate


