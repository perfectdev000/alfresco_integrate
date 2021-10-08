import nltk, string, numpy
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import argparse
import os.path
from os import path
from pathlib import Path

def read_File(file):
     with open(file, encoding="utf-8") as fd:
         data = fd.read()
     return data

def write_File(file, text):
     f=open(file,'w', encoding='utf-8')
     f.write(text)
     f.close()

#nltk.download('punkt') # first-time use only
stemmer = nltk.stem.porter.PorterStemmer()
#nltk.download('wordnet') # first-time use only
lemmer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemTokens(tokens):
     return [lemmer.lemmatize(token) for token in tokens]

def LemNormalize(text):
     return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

LemVectorizer = CountVectorizer(ngram_range=(1, 1),tokenizer=LemNormalize, stop_words='english')

def Lemword(word):
    try:
        LemVectorizer_fit=LemVectorizer.fit_transform(word)
        terms=LemVectorizer.get_feature_names()
        return str(terms[0]) 
    except:
        return ''

def preprocess(text):
    result=''
    parWord=''
    words=word_tokenize(text)
    for word in words:
        if (len(word) > 1):
            wordDoc=[]
            wordDoc.append(word.lower())
            lemmaWord=Lemword(wordDoc)
            if(len(lemmaWord)>1):
                 result=result+lemmaWord+' '               
        if(text.startswith(parWord+word+' ')):
            parWord=parWord+word+' '
        else:
            parWord=parWord+word
    return result
    

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
                    text=preprocess(data)
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





