from random import randint
#from matplotlib import pyplot
# from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import math
import operator
import datetime
from operator import sub
import sqlite3 as sql3
import random
from nltk.corpus import stopwords
import hmm_tagger
from string import punctuation
import i_sentiment_weighting

numpopulation = 5
numdoc = 4
K = randint(3,10)
D = [["",0] for i in range(0,numdoc)]
LittleDelta = 0.0001
f_word_dictionary = []

def peb_tag(word):
	splitted_word = []
	splitted_word = word.split("/")
	return splitted_word

def swn_tag(pos_tag):	
	if (pos_tag == "VB" or pos_tag == "VBD" or pos_tag == "VBT" or pos_tag == "VBG" or pos_tag == "VBN" or pos_tag == "VBP" or pos_tag == "VBZ" or pos_tag == "VBI"):
		return "v"
	elif (pos_tag == "NN" or pos_tag == "NNS" or pos_tag == "NNP" or pos_tag == "NNPS" or pos_tag == "NNG" or pos_tag == "FW" or pos_tag == "MD" or pos_tag == "NNG" or pos_tag == "NNPP" or pos_tag == "WP"):
		return "n"
	elif (pos_tag == "RB" or pos_tag == "RBR" or pos_tag == "RBS" or pos_tag == "NEG" or pos_tag == "SC"):
		return "r"
	elif (pos_tag == "JJ" or pos_tag == "JJR" or pos_tag == "JJS" or pos_tag == "CDC" or pos_tag == "CDI" or 		  pos_tag == "CDO" or pos_tag == "CDP"):
		return "a"
	else:
		return "o"

def remove_punctuation(sentence):
	punctuations = punctuation + '1','2','3'
	for p in punctuation:
		sentence = sentence.replace(p,' ')
	sentence.replace('2',' ')
	return sentence

def open_word_dictionary():
	global f_word_dictionary
	f = open('f_word_dictionary')
	f_word_dictionary = f.read().split("\n")
	f.close()

def remove_numeric(word):
	for i in range(0,10):
		word = word.replace(str(i)," ").lstrip().rstrip()

	return word 

def translate_word(sentence):
	global f_word_dictionary
	clean_sentence = ""
	for item in f_word_dictionary:
		word = item.split("|")
		
		try:
			sentence = sentence.replace(word[0], word[1])
		except:
			print word
			return
		
	sentence = remove_numeric(sentence)
	return sentence 

def preprocess(numdoc, D):
	wordlist = []
	tfcorpus = []
	j = 0 #jumlah kata
	k = 0

	f_wordlist = open('f_wordlist', 'w')

	open_word_dictionary()
	for doc in D:
		cleaned_sentence = translate_word(remove_punctuation(str(doc[1]).lower())) #remove punctuation then lowered the word coz lower is pain, but pain is good
	
		tagged_sentence = hmm_tagger.do_tag(cleaned_sentence) #tag it first, before preprocess
		wordindoc = tagged_sentence.split(" ")
		# print doc
		for word in wordindoc:
			splitted_word = peb_tag(word) #translate to  Peb tag
			theword = splitted_word[0]
			try:
				postag = splitted_word[1] #get  Peb tag
			except:
				print "the word:",splitted_word
			swntag = swn_tag(postag) #get swn tag
			
			if theword not in stopwords.words('indonesian') and not theword.isdigit() and swntag != "o" : #remove stop words in bahasa 
				wordplustag = theword+"|"+swntag
				if wordplustag not in wordlist:
					wordlist.append(wordplustag)
					item = [wordplustag,1]
					tfcorpus.append(item)
					f_wordlist.write(wordplustag+"\n")
					j+=1
				else:
					indeks = wordlist.index(wordplustag)
					tfcorpus[indeks][1] += 1
		k += 1
	

	f_wordlist.close()
	print "jumlah doc", len(D)
	print "jumlah kata", len(wordlist)
	
	return

def Weighting():
	f1 = open('f_wordlist','r')
	f_wordlist = f1.read()
	f2 = open('f_wordlist_weighted','w')

	for word in f_wordlist.split("\n"):
		if word.lstrip().rstrip() != "":
			sentiment  = i_sentiment_weighting.word_weighting(word)
			word_splitted = word.split("|")
			theword = word_splitted[0]
			
			f2.write(word+"|"+str(sentiment[0])+"|"+str(sentiment[1])+"|"+str(sentiment[2])+"|"+str(sentiment[3])+"|"+str(sentiment[4])+"\n")	

	f1.close()
	f2.close()



	return

def do_tfidf(numdoc, D):
	f_wordlist = []
	tfcorpus = []
	j = 0 #jumlah kata
	k = 0

	f1 = open('f_wordlist','r')
	f_wordlist = f1.read().split("\n")
	f1.close()
	
	f2 = open('f_wordlist_weighted_refined','r')
	f_wordlist_weighted = f2.read().split("\n")
	f2.close()

	open_word_dictionary()
	# f3 = open('f_wordlist_weighted_all','rw')
	# f_wordlist_weighted_all = f3.read()
	# f3.close()
	print "Jumlah term: ", len(f_wordlist)
	j = len(f_wordlist)

	bow = [[[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0] for m in range(0, j)] for n in range(0, numdoc)] 
	#1 TP
	#2 TF
	#3 IDF
	#4 TFIDF
	#5 pos
	#6 neg
	#7 obj
	arrayoftfidf = [[[0.0] for m in range(0, j)] for n in range(0, numdoc)]
	m = 0 #bow
	n = 0 #dokumen

	#Hitung TP

	for doc in D:
		try:
			# print n
			cleaned_sentence = translate_word(remove_punctuation(str(doc[1]).lower())) #remove punctuation then lowered the word coz lower is pain, but pain is good

			tagged_sentence = hmm_tagger.do_tag(cleaned_sentence) #tag it first, before preprocess
			
			wordindoc = tagged_sentence.split(" ")
			
			for word in wordindoc:
				
				splitted_word = peb_tag(word) #translate to sensei Peb tag
				
				# if len(splitted_word)==2:
				theword = splitted_word[0]
				try:
					postag = splitted_word[1] #get sensei Peb tag
				except:
					print splitted_word
					continue
				swntag = swn_tag(postag) #get swn tag
				
				if theword not in stopwords.words('indonesian') and not theword.isdigit() and swntag != "o" : #remove stop words in bahasa 
					wordplustag = theword+"|"+swntag
					try:
						if wordplustag in f_wordlist:
							indeks = f_wordlist.index(wordplustag)
					except:	
						indeks = -1
							
					if indeks >= 0:	
						wordlist_weigted = 	 f_wordlist_weighted[indeks].split("|")
						# print n,word.lower()
						# print "gotchaa"
						bow[n][indeks][0] += 1
						# print bow[n][indeks][0]
						bow[n][indeks][4] = wordlist_weigted[4]
						bow[n][indeks][5] = wordlist_weigted[5]
						bow[n][indeks][6] = wordlist_weigted[6]				
						bow[n][indeks][7] = wordlist_weigted[7]
			n+=1
		except:
			print "Empty content... #1"
			continue
	#Hitung MaxTF
	i = 0
	for doc in D:
		try:
			maxtf = 0
			for item_bow in bow[i]:
				if maxtf < item_bow[0]:
					maxtf = item_bow[0]

			D[i][1] = maxtf
			i+=1
		except:
			print "Empty content... #2"
			continue
	#Hitung TF
	i = 0
	for doc in D:
		try:
			maxtf = 0
			for item_bow in bow[i]:
				try:
					item_bow[1] = item_bow[0] / D[i][1]
				except:
					item_bow[1] = 0.0
						# print "error"	
			i+=1
		except:
			print "Empty content... #3"
			continue
	#Hitung IDF & TFIDF
	i = 0
	n = 0
	for doc in D:
		# try:
		maxtf = 0
		n = 0
		for item_bow in bow[i]:
			if item_bow[0] > 0:
				try:
					item_bow[2] = math.log(numdoc/item_bow[0])
					item_bow[3] = item_bow[1] * item_bow[2]
					# if item_bow[4] >= item_bow[5]:
					# 	pos_neg = 1
					# else:
					# 	pos_neg = -1

					pos_neg = item_bow[7]
					arrayoftfidf[i][n] = item_bow[3] * float(pos_neg)
				except:
					arrayoftfidf[i][n] = 0.0
					# print "error"
			else:
				arrayoftfidf[i][n] = 0.0
			n+=1
		i+=1
		# except:
		# 	print "Empty content..."
		# 	continue 
	bowt = open('f_bag_of_weighted_terms','w+')

	bag_of_weighted_terms = arrayoftfidf

	for d in bag_of_weighted_terms:
		for wt in d:
			bowt.write(str(wt).rstrip().lstrip() + " ")
		bowt.write(";")
	bowt.close()
	return arrayoftfidf

def Generate_Population(K, numpopulation, numdoc):
	population = [[randint(0,K) for i in range(0,numdoc)] for j in range(0,numpopulation)]
	return population
	
def Average_Fitness(population, numpopulation, numdoc):
	Affinity = 0.0
	RawAffinity = 0.0001 
	AverageAffinity = 0.0
	SumAffinity = 0.0
	for index, cell in enumerate(population):
		if index+1 < numpopulation:
			for i in range(index, numpopulation-1):
				population[index].sort()
				population[i+1].sort()
				C = map(sub, population[index], population[i+1]) #cari perbedaan cell satu dengan yag lain
				# print index, " dengan ", i+1
				RawAffinity = float(len(set(filter(lambda a: a!=0, C)))) #hilangkan affinity = 0 dgn lambda exp. hitung selainnya

				Affinity = RawAffinity / numdoc #hitung affinity 
				SumAffinity += Affinity
				# print Affinity
				i+=1
	AverageAffinity = SumAffinity / (numpopulation * 2)				
	return AverageAffinity

def do_the_magic():
	global numdoc
	numdoc = 0
	corpus = []
	corpus_content = []
	conn = sql3.connect('DB_WORDS')
	c = conn.cursor()
	sql = 'select c1.id, ifnull(cont1," ") || " " || ifnull(cont2," ") || " " || ifnull(cont3," ") || " " || ifnull(cont4," ") || " " || ifnull(cont5," ") || " " || ifnull(cont6," ") || " " || ifnull(cont7," ") || " " || ifnull(cont8," ") as content  from '
	sql += '(select id,"" as cont0 from mst_opini_mitigasi_raw group by id ) c0 left join '
	sql += "(select id,content as cont1 from mst_opini_mitigasi_raw where opini_mitigasi = 1 and part = 1) c1 on c0.id = c1.id  left join "
	sql += "(select id,content as cont2 from mst_opini_mitigasi_raw where opini_mitigasi = 1 and part = 2) c2 on c0.id = c2.id  left join "
	sql += "(select id,content as cont3 from mst_opini_mitigasi_raw where opini_mitigasi = 1 and part = 3) c3 on c0.id = c3.id  left join "
	sql += "(select id,content as cont4 from mst_opini_mitigasi_raw where opini_mitigasi = 1 and part = 4) c4 on c0.id = c4.id  left join "
	sql += "(select id,content as cont5 from mst_opini_mitigasi_raw where opini_mitigasi = 1 and part = 5) c5 on c0.id = c5.id  left join "
	sql += "(select id,content as cont6 from mst_opini_mitigasi_raw where opini_mitigasi = 1 and part = 6) c6 on c0.id = c6.id  left join "
	sql += "(select id,content as cont7 from mst_opini_mitigasi_raw where opini_mitigasi = 1 and part = 7) c7 on c0.id = c7.id  left join "
	sql += "(select id,content as cont8 from mst_opini_mitigasi_raw where opini_mitigasi = 1 and part = 8) c8 on c0.id = c8.id "

	print sql
	f = open('f_doc_map','w+')
	bag_of_rows = c.execute(sql)
	for bor in bag_of_rows:		
		
		if str(bor[0]).isdigit():
			numdoc+=1
			f.write(str(bor[0]) +  ":" + str(numdoc) + "\n")
			corpus_content= [bor[0],str(bor[1]),0]
			corpus.append(corpus_content)
	f.close()
	return corpus


print datetime.datetime.now()
# print "Start clustering with K = ", K
# D = do_the_magic()
# preprocess(0,D)
# Weighting()
# arrayoftfidf = do_tfidf(numdoc, D)
print datetime.datetime.now()


