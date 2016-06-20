from random import randint
#from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import math
import operator
import nltk
from nltk import bigrams, trigrams

def K_Means(K, P):
	#ambil random indeks untuk tentukan anggota dari P yang dijadikan centroid
	DataRowNum = len(P)
	AttributeNum = len(P[0])
	R = [0] * K
	C = [[0 for attributenum in range(AttributeNum)] for KNum in range(K)]

	# print C
	for i in range(0, K):
		R[i] = randint(0,DataRowNum - 1)
		C[i] = P[R[i]]
		# print('Centroid ' + str(i+1) + ' : P' + str(R[i]))
		# print('Data : C[' + str(i+1) + ']' + str(C[i]))

	D = [[0 for x in range(K)] for x in range(DataRowNum)]
	CG = [0 for x in range(DataRowNum)]

	TMPATTRC = [[0 for x in range(AttributeNum)] for x in range(K)]
	CNTMEMBERC = [0 for x in range(K)]

	maxiteration = 100 #coba sampai 100 kali iterasi
	iteration = 0
	# G = [[0 for x in range(4)] for x in range(10)]
	GTEMP = [[0 for x in range(K)] for x in range(DataRowNum)]
	for i in range(0,maxiteration): #percobaan i dari 0 hingga ke  maxiteration

		G = [[0 for x in range(K)] for x in range(DataRowNum)]
		for x in range (0,DataRowNum): #hitung jarak euclid untuk masing-masing atribut	
			for y in range(0,AttributeNum - 1):
				for z in range (0, K):
					D[x][z] += math.sqrt(math.pow(P[x][y] - C[z][y],2))
		


		for x in range (0, DataRowNum):
			DISTTOCOMPARE = D[x]
			MINDIST = DISTTOCOMPARE.index(min(DISTTOCOMPARE))
			CG[x] = MINDIST
			# print DISTTOCOMPARE
			# print MINDIST
			G[x][MINDIST] = 1
			TMPATTRC[MINDIST] = map(sum, zip(TMPATTRC[MINDIST],P[x])) 
			# print 'P[',str(x),'] = ', P[x]
			# print 'TMPATTRC[',str(MINDIST),'] = ', TMPATTRC[MINDIST]
			
			CNTMEMBERC[MINDIST] += 1

		for z in range(0, K):
			if CNTMEMBERC[z] > 0:
				C[z][:] = [v / CNTMEMBERC[z] for v in C[z]]

		print "G ", G
		print "GTEMP ", GTEMP
		if np.array_equal(G,GTEMP):
			break
		
	 	GTEMP = G

	print "Iteration ", i

def TFIDF(numdoc, D):
	wordlist = ["" for i in range(0,1000)]
	tfcorpus = [["",1] for i in range(0,1000)]
	j = 0
	k = 0

	for doc in D:
		wordindoc = doc[0].split(" ")
		for word in wordindoc:
			if word.lower() not in wordlist:
				wordlist[j] = word.lower()
				tfcorpus[j][0] +=  word.lower() 								
				tfcorpus[j][1] += 1		
				j+=1
			else:
				indeks = wordlist.index(word.lower())
				tfcorpus[indeks][1] += 1

	# for k in range(0,j):
	# 	print k, "-", tfcorpus[k]

	bow = [[[0.0,0.0,0.0,0.0] for m in range(0, j)] for n in range(0, numdoc)]
	arrayoftfidf = [[[0.0] for m in range(0, j)] for n in range(0, numdoc)]
	m = 0 #bow
	n = 0 #dokumen

	#Hitung TP
	for doc in D:
		wordindoc = doc[0].split(" ")
		print "wordindoc", wordindoc
		for word in wordindoc:
			if word.lower()  in wordlist:
				indeks = wordlist.index(word.lower())
				print n,word.lower()
				bow[n][indeks][0] += 1
		n+=1

	#Hitung MaxTF
	i = 0

	for doc in D:
		maxtf = 0
		for item_bow in bow[i]:
			if maxtf < max(item_bow):
				maxtf = max(item_bow)
		D[i][1] = maxtf
		i+=1

	#Hitung TF
	i = 0
	for doc in D:
		maxtf = 0
		for item_bow in bow[i]:
			item_bow[1] = item_bow[0] / D[i][1]
		D[i][1] = maxtf
		i+=1

	#Hitung IDF & TFIDF
	i = 0
	n = 0
	for doc in D:
		maxtf = 0
		n = 0
		for item_bow in bow[i]:
			if item_bow[0] > 0:
				item_bow[2] = math.log(numdoc/item_bow[0])
				item_bow[3] = item_bow[1] * item_bow[2]
				arrayoftfidf[i][n] = item_bow[3]
			else:
				arrayoftfidf[i][n] = 0.0
			n+=1
		D[i][1] = maxtf
		i+=1


	# for item in arrayoftfidf:
	# 	print item,"\n"
	return arrayoftfidf


numdoc = 4
D = [["",0] for i in range(0,numdoc)]
# D[0][0] = "Sebagian sebagian dari rasio likuiditas dan profitabilitas calon debitur menunjukkan trend yang melemah"
# D[1][0] = "Sebagian dari rasio likuiditas dan profitabilitas calon debitur menunjukkan trend yang yang yang melemah"
# D[2][0] = "Sebagian rasio keuangan terkait aktivitas dan profitabilitas mengalami tren melemah Rasio likuiditas dan sebagian rasio likuiditas memiliki kinerja yang lebih rendah dari kisaran kinerja industri sejenis"
# D[3][0] = "Lengkap namun terindikasi pemilihan benchmark sektor usaha kurang tepat seharusnya dilakukan benchmark terhadap sektor perdagangan sparepart mobil sehingga rating tersebut diatas belum sepenuhnya mencerminkan tingkat risiko calon debitur"
# D[4][0] = "Agar dipastikan mengenai kebenaran data yang telah diinput dalam ICRR oleh AO / Analis Kredit. Selanjutnya harus terus dilakukan updating informasi fasilitas kredit dan dilengkapi dengan laporan keuangan terbaru, terutama untuk menghindari adanya pengambilan keputusan kredit dengan dasar pertimbangan yang tidak akurat 2.2.	Rasio yang terkait Profitabilitas memiliki tren melemah. Selain itu sebagian rasio aktivitas lebih lemah dibanding kisaran benchmark perusahaan sejenis. Agar diperhatikan risiko yang mungkin timbul apabila hal tersebut terus berlanjut, dan dipastikan upaya monitoring yang harus dilakukan untuk meminimalisir risiko tersebut"
D[0][0] = "the sky is blue"
D[1][0] = "the sun is shining bright in the sky"
D[2][0] = "my heart is in blue because of your shine"
D[3][0] = "my heart will go on and shining blue"



# arrayoftfidf = TFIDF(numdoc, D)

# print arrayoftfidf
# K_Means(3, arrayoftfidf)


stopwords = ['for', 'is', 'of']
stopwords.extend(nltk.corpus.stopwords.words('indonesian'))
stopwords.extend(nltk.corpus.stopwords.words('english'))