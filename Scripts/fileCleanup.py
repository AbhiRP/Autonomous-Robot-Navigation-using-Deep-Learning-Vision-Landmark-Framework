#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Created by Abhi Ravikumar (abhi.ravikumar@protonmail.com)
# Graduate Students @ The University of Texas at San Antonio, TX U.S.A
# Research Students @ Autonomous Control & Engineering (ACE) Laboratory at UTSA
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import csv
#Cleaning empty rows
input = open('Textspeech.csv', 'rb')
output = open('Tempfile.csv', 'wb')
writer = csv.writer(output)
for row in csv.reader(input):
    if row:
        writer.writerow(row)
input.close()
output.close()

#Deleting unnecessary 2nd and 3rd columns
with open("Tempfile.csv","rb") as source:
    rdr= csv.reader( source )
    with open("NewFile.csv","wb") as result:
        wtr= csv.writer( result )
        for r in rdr:
            wtr.writerow( (r[0:1]) )
