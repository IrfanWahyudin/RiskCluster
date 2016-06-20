import sys
import numpy as np
import math
import matplotlib.pyplot as mlp
from itertools import izip
# import i_evaluation as ev
# import i_k_means as k
import hmm_tagger

from nltk.corpus import stopwords
from string import punctuation
f_word_dictionary = []

def read_doc_map():
	doc_map = []
	f = open('f_doc_map','r')
	f_doc_map = f.read().split('\n')

	for d in f_doc_map:
		dm = d.split(":")
		doc_map.append([dm[1],dm[0]])
	return doc_map

def replace_to_one(v):
	if v != 0.0:
		return 1
	else:
		return 0

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
	elif (pos_tag == "JJ" or pos_tag == "JJR" or pos_tag == "JJS" or pos_tag == "CDC" or pos_tag == "CDI" or pos_tag == "CDO" or pos_tag == "CDP"):
		return "a"
	else:
		return "o"
def open_word_dictionary():
	global f_word_dictionary
	f = open('f_word_dictionary')
	f_word_dictionary = f.read().split("\n")
	f.close()
def translate_word(sentence):
	global f_word_dictionary
	clean_sentence = ""
	for item in f_word_dictionary:
		word = item.split("|")
		
		try:
			sentence = sentence.replace(word[0], word[1])
		except:
			# print word
			return
		
	sentence = remove_numeric(sentence)
	return sentence 
def remove_punctuation(sentence):
	punctuations = punctuation + '1','2','3'
	for p in punctuation:
		sentence = sentence.replace(p,' ')
	sentence.replace('2',' ')
	return sentence
def remove_numeric(word):
	for i in range(0,10):
		word = word.replace(str(i)," ").lstrip().rstrip()

	return word 
def tag_word(the_sentence):
	word_with_tag = []
	open_word_dictionary()
	cleaned_sentence = translate_word(remove_punctuation(str(the_sentence).lower()))

	tagged_sentence = hmm_tagger.do_tag(cleaned_sentence) 
	wordindoc = tagged_sentence.split(" ")
	
	for word in wordindoc:
		splitted_word = peb_tag(word) #translate to  Peb tag
		theword = splitted_word[0]
		try:
			postag = splitted_word[1] #get  Peb tag
		except:
			continue
			# print "the word:",splitted_word
		swntag = swn_tag(postag) #get swn tag

		if theword not in stopwords.words('indonesian') and not theword.isdigit() and swntag != "o" : #remove stop words in bahasa 
			wordplustag = theword+"|"+swntag
			if wordplustag not in word_with_tag:
				word_with_tag.append(wordplustag)

	return word_with_tag

	
def replace_to_one(v):
	if v != 0.0:
		return 1
	else:
		return 0
def lsi(bowt):
	A = []	
	# docs = ["Romeo and Juliet","Juliet O happy dagger","Romeo died by dagger","Live free or die thats the New-Hampshire motto","Did you know New-Hampshire is in New England"]

	# wordlist = ["romeo","juliet","happy","dagger","live","die","free","new-hampshire"]


	# for d in docs:
	#     wv = [0 for x in range(0,len(wordlist))]
	#     for i,w in enumerate(wordlist):
	#         if w in d.lower():
	#             wv[i] = 1
	#     A.append(wv)
	# A = np.array(A).transpose()
	
	
	A = np.array(bowt[:-1]).transpose()
	# print A.shape
	
	SA, EA, UA = np.linalg.svd(A, full_matrices=True)
	SA = SA.transpose()
	
	# print sum(EA[:300].tolist()) / sum(EA) 
	
	# print SA #Eigen Vector B
	# print EA #Eigen Value B
	# print UA #Eigen Vector C

	# print EA[:300]
	# print SA[:300]
	# print UA[:300]

	SAS = SA[:300]
	EAS = EA[:300]
	UAS = UA[:300]

	EAn = EAS.tolist()
	# print EAn
	EAL = [[0.0 for x in range(0, len(EAn))] for x in range(0, len(EAn))]
	for x in range(0, len(EAn)):
	    for y in range(0, len(EAn)):
	        if x==y:
	            EAL[x][y] = EAn[x]
	EAS = np.array(EAL)

	w = np.dot(SAS.transpose(), EAS)
	d = np.dot(EAS.transpose(), UAS)
	# print w.tolist()
	# print d.transpose().tolist()
	w = w.tolist()
	d = d.transpose().tolist()

	# print len(d)

	###################################################################
	#		Begin Query
	###################################################################
	print "pass query"
	f1 = open('f_wordlist','r')
	wordlist = f1.read().split('\n')
	f1.close()
	query_terms = word_with_tag
	num_of_query = 0
	args=[]
	args_index=[]
	for i, arg in enumerate(query_terms): 
		if i>0:		
			for j, word in enumerate(wordlist):
				if arg == word and arg not in args:							
					args.append(word)			
					args_index.append(j)
					num_of_query+=1	
	if num_of_query > 0:
		print "pass query 1"
		temp_sum = np.zeros(300)

		for q in args_index:
			temp_sum = np.add(np.array(temp_sum), np.array(w[q])) 

		# q = np.divide(np.add(np.array(word1), np.array(word2)), num_of_query)
		
		q = np.divide(temp_sum, num_of_query)
		# print "q", q
		a = q

		query_result = []
		for i in range(0,518):
			b = d[i]

			prod = sum(map(lambda x: x[0] * x[1], izip(a, b)))
			len1 = math.sqrt(sum(map(lambda x: x[0] * x[1], izip(a, a))))
			len2 = math.sqrt(sum(map(lambda x: x[0] * x[1], izip(b, b))))

			query_result.append([i, prod / (len1 * len2)])

		query_result_sorted = sorted(query_result, key=lambda x: x[1], reverse= True)

		doc_map = read_doc_map()
		print "|"
		for j in range(0,518):
			print query_result_sorted[j][0],">", doc_map[query_result_sorted[j][0]-1][1]
			print "|"


	#*************************************
	#Try die, dagger:
	#*************************************
	# print w
	# print d
	# word1 = w[7]
	# word2 = w[1]
	# print word1,word2
	
	# q = np.divide(np.add(np.array(word1), np.array(word2)), 2)
	# print "q",len(q)
	# query_result = []
	# for dcount in range(0,len(d)):
	# 	a = word1
	# 	b = d[dcount]

	# 	# print a
	# 	# print b

	# 	prod = sum(map(lambda x: x[0] * x[1], izip(a, b)))
	# 	len1 = math.sqrt(sum(map(lambda x: x[0] * x[1], izip(a, a))))
	# 	len2 = 1#math.sqrt(sum(map(lambda x: x[0] * x[1], izip(b, b))))

	# 	if len1 ==0 or len2 == 0:
	# 		query_result.append(0.0)
	# 		print dcount, "|", 0.0
	# 	else:
	# 		query_result.append(prod / (len1 * len2))
	# 		print dcount, "|", prod / (len1 * len2)

	# for item in d:
	# 	mlp.plot(item[01],item[1],'g^')

	# for item in w:
	# 	mlp.plot(item[0],item[1],'r*')
	# mlp.show()
	# print d
	# return d

def main(word_with_tag):
	f = open('f_bag_of_weighted_terms')
	weighted_terms = f.read().split('\n')
	f.close()

	f = open('f_wordlist')
	wordlist = f.read().split('\n')
	f.close()

	bag_of_weighted_terms = []
	member_list = []

	for wt in weighted_terms:
		bag_of_weighted_terms.append([replace_to_one(float(x)) for  x in wt[:-1].split(',') if x != ''])

	f = open('f_term_presence_matrix','w+')
	for bowt in bag_of_weighted_terms:
		for tp in bowt:
			f.write(str(tp) + ',')
		f.write('\n')
	f.close()

	P = lsi(bag_of_weighted_terms)

	return P

num_of_query = 0
sentence_query = ""
for i, arg in enumerate(sys.argv): 
	if i>0:
		sentence_query += " " + arg

# sentence_query = "risiko tinggi"
word_with_tag = tag_word(sentence_query)
# print sentence_query
# print sys.argv
# print "word_with_tag",	word_with_tag
main(word_with_tag)
# A = [1,2,3,4,5,6]
# print A[2:]
