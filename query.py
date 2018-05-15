import xml.etree.ElementTree as ET 					#for extracting text from XML
import string
import pickle
import timeit
import glob
import operator
import math
from nltk import PorterStemmer
from nltk.corpus import stopwords
def main():
	global exclude,i,queryDict,indexDict,num
	indexDict=pickle.load(open('wordI.pickle','rb'))			#index of all the file docs generated from create_index.py
	noOfDocs=20000
	exclude = list(string.punctuation)

	file = open("result.txt", 'w')
	root=ET.parse('en.topics.126-175.2011.txt').getroot()		#contains all the test queries
	for q in root.findall("top"):
		queryDict = {}			
		num=q.find('num').text
		title=q.find('title').text
		desc=q.find('desc').text
		text=title+" "+desc
		text = remove_punctuation(text.lower())
		words = remove_stopwords(text)
		stemmed_words = [PorterStemmer().stem(w) for w in words]        #array of words stemmed
		write_to_dictionary(words)
		
		docsArray={}
		for word in queryDict:
			if word in indexDict:
				for docName in indexDict[word]:
					idf=math.log(noOfDocs/len(indexDict[word]))
					if str(docName) in docsArray:
						docsArray[str(docName)]+=indexDict[word][docName]*idf*queryDict[word]
					else:
						docsArray[str(docName)]=indexDict[word][docName]*idf*queryDict[word]

		sorted_docs = sorted(docsArray.items(), key=operator.itemgetter(1),reverse=True)
		counter=0
		for i in sorted_docs:
			counter+=1
			print(num+" Q0 "+i[0]+" "+str(counter)+" "+str(i[1]))
			file.write(num+" Q0 "+i[0]+" "+str(counter)+" "+str(i[1])+"\n")
	file.close()

def write_to_dictionary(word):							#stores all the words in dictionary 
	wordUnique = list(set(word))						#remove duplicate words
	for j in range(len(wordUnique)):
		queryDict[str(wordUnique[j])]=word.count(str(wordUnique[j]))	#if new word comes up, create new list 
	#print(queryDict)

def remove_stopwords(text):							#returns an array of words removing stopwords
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
	main()
