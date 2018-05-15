#This file creates 
import xml.etree.ElementTree as ET 								#for extracting text from XML
import string
import pickle
import timeit
import glob
import os.path
from nltk import PorterStemmer
from nltk.corpus import stopwords

def main():
	start = timeit.default_timer()								#code starts running here, calculting run time
	global exclude,i,docID
	exclude = list(string.punctuation)
	docID = 0
	docs=glob.glob("en.docs.2011/**/*",recursive=True)					#contains all the docs
	for i in docs:
		try:
			root = ET.parse(i).getroot()
			text=""
			for j in root.findall('TITLE'):
				text+=j.text
			for j in root.findall('TEXT'):
				text+=j.text
			text = remove_punctuation(text.lower())
			words = remove_stopwords(text)
			stemmed_words = [PorterStemmer().stem(w) for w in words]    		#array of words stemmed
			write_to_dictionary(stemmed_words)
			docID+=1
			print(docID)
		except Exception as e:
			print(e)
			print(i)
			docID+=1
	print (timeit.default_timer() - start)							#total run time of code
	pickle.dump(indexDict,open('wordI.pickle','wb'),protocol=pickle.HIGHEST_PROTOCOL)	#convert to byte stream,highest protocol means maximum compression
	print (timeit.default_timer() - start)							#run time of dump

def write_to_dictionary(word):							#stores all the words in dictionary 
	wordUnique = list(set(word))						#remove duplicate words
	documentLength=len(word)
	for j in range(len(wordUnique)):
		tf=word.count(str(wordUnique[j]))/documentLength
		if str(wordUnique[j]) in indexDict.keys():
			indexDict[str(wordUnique[j])].append((os.path.basename(i),tf))
		else:
			indexDict[str(wordUnique[j])] = [(os.path.basename(i),tf)]		#if new word comes up, create new list 
	#print(indexDict)

def remove_stopwords(text):								#returns an array of words removing stopwords
	stopWords = set(stopwords.words('english'))				#list of stopWords
	words = []
	text = text.split()
	for c in text:
		if c not in stopWords:
	 		words.append(c)
	return words

def remove_punctuation(text):							#returns a string without punctutations
	text = "".join(char for char in text if char not in exclude) 
	return text

if __name__ == '__main__':
	indexDict = {}							#dictionary storing document IDs of all words
	main()
