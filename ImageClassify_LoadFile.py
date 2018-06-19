import subprocess
import glob2
import sys
from shutil import copyfile
import pathlib
import sqlite3
import os

#Specify Source Dir
sourcedir = "C:/Users/Username/Desktop/ImageClassify/source"
#Specify Outpur Dir
outputdir = "C:\\Users\\Username\\Desktop\\ImageClassify\\output\\"
#Create natives directory in output dir
if not os.path.isdir(outputdir+'NATIVES'):
    os.mkdir(outputdir+'NATIVES')
#Create text directory in output dir
if not os.path.isdir(outputdir+'TEXT'):
    os.mkdir(outputdir+'TEXT')
count = 1 #initialize counter

#populate load file column headings
open(outputdir+"loadfile.dat","w").close()
sys.stdout = open(outputdir+"loadfile.dat","a")
print("\xFEDOCID\xFE\x14\xFEName\xFE\x14\xFEPath\xFE\x14\xFETopPrediction\xFE\x14\xFETopPredictionScore\xFE\x14\xFEITEM_PATH\xFE\x14\xFETEXT_PATH\xFE")
open(outputdir+"loadfile.dat").close()

#create database and tables
conn = sqlite3.connect(outputdir+"imageclassify.db")
c = conn.cursor()
def create():
	try:
		c.execute("""CREATE TABLE FilesTable(DOCID, Name, OrigPath, NewPath)""")
	except:
		pass
	try:
		c.execute("""CREATE TABLE FilePredictionTable(DOCID, Prediction, Score NUMERIC)""")
	except:
		pass
def tableclear():
	c.execute("""DELETE from FilesTable""")
	c.execute("""DELETE from FilePredictionTable""")
create()
tableclear()

#Recurse through files in input directory
for file in glob2.glob(sourcedir + "/**/*.*", recursive=True): 
	command = "ntpq -p"  #shell commend
	outputtextdir = outputdir+"TEXT\\" 
	outputnativesdir = outputdir+"NATIVES\\" 
	origpath = file.replace("/","\\")
	countpadded = "URN"+format(count, '08d') #Assign sequential numerical reference
	command ="classify_image.py --image_file="+"\""+origpath+"\" > \""+outputtextdir+countpadded+".txt\"" #shell command
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True) 
	copyfile(origpath,outputnativesdir+countpadded+pathlib.Path(origpath).suffix) # name copies of original files by numerical ref
	output = process.communicate()
	outputtxtfile = outputtextdir+countpadded+".txt"
	nativepath = "NATIVES\\"+countpadded+pathlib.Path(origpath).suffix
	textpath = "TEXT\\"+countpadded+".txt"
	topprediction = open(outputtxtfile).readline().split(" (")[0]
	topscore = open(outputtxtfile).readline().split(" (")[1].replace("score = ","").replace(")\n","")
	
#populate load file
	sys.stdout = open(outputdir+"loadfile.dat","a")
	print("\xFE"+countpadded+"\xFE\x14\xFE"+pathlib.Path(origpath).name+"\xFE\x14\xFE"+origpath+"\xFE\x14\xFE"+topprediction+"\xFE\x14\xFE"+topscore+"\xFE\x14\xFE"+nativepath+"\xFE\x14\xFE"+textpath+"\xFE")
	open(outputdir+"loadfile.dat").close()
	
#populate SQLITE database
	def insertF(): #insert into files table
		c.execute("INSERT INTO FilesTable (DOCID, Name, OrigPath, NewPath) VALUES(?,?,?,?)", (countpadded, pathlib.Path(origpath).name, origpath,"NATIVES\\"+countpadded+pathlib.Path(origpath).suffix))
	insertF()
	conn.commit() 
	def insertFP(): #insert into file predictions table
		c.execute("INSERT INTO FilePredictionTable (DOCID, Prediction, Score) VALUES(?,?,?)", (countpadded, line.split(" (")[0], line.split(" (")[1].replace("score = ","").replace(")\n","")))
	f = open(outputtxtfile)
	lines = f.readlines()
	for line in lines:
		insertFP()
		conn.commit() 
	f.close()
#Increment sequential counter
	count = count+1 
	


	