import argparse
import os.path
from os import path
from pathlib import Path
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize
import re
import multiprocessing.pool as pool
from multiprocessing.pool import ThreadPool

def read_File(file):
     with open(file, encoding="utf-8") as fd:
         data = fd.read()
     return data

def write_File(file, text):
     f=open(file,'w', encoding='utf-8')
     f.write(text)
     f.close()

spell=SpellChecker()
def checkword(word):
     if(len(word)>1):
          result=str(spell.correction(word))
          wordL=word.replace('-','')
          wordC= word.count('-')
          if(wordC==1 and word.lower()!=result and wordL.lower()==result):
               return wordL
          elif(wordC==2 and word.lower()!=result and wordL.lower()==result.replace('-','')):
               return result
     return ''

seg_length = 25
p = pool.ThreadPool(seg_length)
def checkwordList(words):
     changeList=[]
     '''
     for word in words:
          result=checkword(word)
          if(len(result)>2):
               changeList.append(word+','+result)          
     return changeList
     '''
     segs=[words[x:x+seg_length] for x in range(0,len(words),seg_length)]
     result=[]     
     for seg in segs:          
          res=(p.map(checkword, seg))          
          result=result+res

     for i in range(len(result)):
          if len(result[i])>0:
               changeList.append(words[i]+','+result[i]) 
     print(changeList)     
     return changeList
         


def hyphenWord(text):
    data=re.sub(r'[^A-Za-z-]+', ' ', text)
    data=re.sub(' +', ' ', data)
    words=word_tokenize(data)
    wordList=[]
    
    for word in words:
        wCount= word.count('-')
        if (word not in wordList and  wCount> 0 and wCount< 3 and len(word)>1):
             wPart=word.split('-')
             if((wCount==2 and len(wPart[0]) > 1 and len(wPart[1]) > 1 and len(wPart[2]) > 1) or (wCount==1 and len(wPart[0]) > 1 and len(wPart[1]) > 1)):
                  wordList.append(word)
                  
    if len(wordList)>0:              
         changeList=checkwordList(wordList)
         for change in changeList:
              part=change.split(',')
              text=text.replace(part[0],part[1])
    return text
     
     


def process(inDir,outDir):
     listFile=[]
     inFiles = os.listdir(inDir)   
     outFiles = os.listdir(outDir)

     for i in outFiles:
          if i.endswith('.txt'):
               listFile.append(i)     

     for i in inFiles:
          if i not in listFile and i.endswith('.txt'):
               print(i)
               data=read_File(inDir+i)
               if len(data)>0:
                    text=hyphenWord(data)
                    write_File(outDir+i,str(text))
    

argument = argparse.ArgumentParser()
argument.add_argument("-i", "--inputDir", type=str, required=True, help="path to input directory")
argument.add_argument("-o", "--outputDir", type=str, required=True, help="path to output directory")
argsParse = vars(argument.parse_args())
inDir=argsParse["inputDir"]
outDir=argsParse["outputDir"]

if not path.isdir(outDir):
     os.makedirs(outDir)
inDir=str(Path(inDir).resolve())+os.path.sep
outDir=str(Path(outDir).resolve())+os.path.sep
process(inDir,outDir)
