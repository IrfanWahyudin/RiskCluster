__author__ = 'irfan'
from random import randint
import numpy as np
import math
import operator
import distance
from operator import itemgetter
def Randomized_Centroids(K, P):
	AttributeNum = len(P[0])
	DataRowNum = len(P)
	C = [[0.0 for attributenum in range(AttributeNum)] for KNum in range(K)]
	R = 0
	
	c_list = [0 for c in range(K)]
	# print len(C)
	pick_done = False
	i = 0
	while (not pick_done):
		R = randint(0,DataRowNum - 1)

		if R not in c_list:
			print "i", R
			C[i] = P[R]
			c_list.append(R)

			i+=1
			if i==K:
				break

	# print('Centroid ' + str(i+1) + ' : P' + str(R[i]))
	# print('Data : C[' + str(i+1) + ']' + str(C[i]))
	return C

def Optimized_Centroids(K, P, alpha, beta):
	#====================================================================#
	#	Adopted from Ali Ridha Barakbah's Paper Pillar Algorithm(2005)
	#	Code written by Irfan Wahyudin and Hermawan Wiryana
	#====================================================================#
	n = len(P)
	NumAttr = len(P[0])

	# alpha = 0.9
	# beta = 0.8
	Centroid = []
	C = None
	SX = None
	DM = []
	nmin = int((alpha * n) / K)
	maxiter = n
	iters = 0
	print alpha, "*", n, "/",K,"=",nmin

	#=====================================
	# Cari mean
	#=====================================
	SumP = [sum(i) for i in zip(*P)]
	m = []
	for sp in SumP:
		temp = float(sp) / n 
		m.append(temp)
	# print m

	Distance = []
	DistanceDM = []
	i = 0
	for p in P:
		d = np.linalg.norm(np.array(p) - np.array(m))
		Distance.append([i, d])
		i+=1

	D = sorted(Distance, key=itemgetter(1), reverse=True)

	# print Distance
	iDist = 0
	SX = []
	DM = []
	print DM

	i = 0
	no = 0.0
	C = []
	DM = D
	while (i<K and iters < maxiter):
		print "back to first object...", i, K, iters, maxiter
		dmax = DM[0][1]
		dmax_index = DM[0][0]
		nbdis = beta * float(dmax)
		
		for x in range(0,n-1):
			try:
				if DM[x][0] not in SX:
					majesty = P[DM[x][0]]
					SX.append(DM[x][0])
					break
			except:
				return


		iDist += 1
		j=0
		Distance = []
		for p in P:
			d = np.linalg.norm(np.array(p) - np.array(majesty))
			Distance.append([j, d])
			j+=1		
		D = sorted(Distance, key=itemgetter(1), reverse=True)

		no = 0
		for dy in D:
			if dy[1] <= nbdis:
				no +=1
		
		if no >= nmin:
			i+=1
			C.append(majesty)
			print "Centroid #",str(i),"Jumlah objek terdekat: ", no, "dari", nmin, "yang diperbolehkan"
			iters = 0
			for p in P:
				d = np.linalg.norm(np.array(p) - np.array(majesty))
				DistanceDM.append([i, d])
			

			DM = sorted(DistanceDM, key=itemgetter(1), reverse=True)
			
		else:
			print "iters",iters,"Sepiii...Jumlah objek terdekat: ", no, "dari", nmin, "yang diperbolehkan"
			iters+=1

		if iters == maxiter:
			print "Iteration exceeds"
			return None
	
	return C


def K_Means(K, P, CMethod, aplha = 0, beta = 0 ):
	#ambil random indeks untuk tentukan anggota dari P yang dijadikan centroid
	DataRowNum = len(P)
	AttributeNum = len(P[0])
	if CMethod == 1:
		#**************************************************************************#
		#			Randomly Pick Centroids
		#**************************************************************************#
		C = Randomized_Centroids(K, P)
	elif CMethod == 2:
		#**************************************************************************#
		#			Carefully Pick Centroids with Pillar Algorithm
		#**************************************************************************#
		C = Optimized_Centroids(K, P, aplha, beta)
		if C == None:
			return [0.0,0.0]

	# print C
	D = [[0 for x in range(K)] for x in range(DataRowNum)]
	CG = [0 for x in range(DataRowNum)]

	TMPATTRC = [[0 for x in range(AttributeNum)] for x in range(K)]
	CNTMEMBERC = [0 for x in range(K)]

	maxiteration = 100 #coba sampai 100 kali iterasi
	iteration = 0
	# G = [[0 for x in range(4)] for x in range(10)]
	GTEMP = [[0 for x in range(K)] for x in range(DataRowNum)]
	has_converged = False
	for i in range(0,maxiteration): #percobaan i dari 0 hingga ke  maxiteration
		if has_converged:
			break

		G = [[0 for x in range(K)] for x in range(DataRowNum)]
		for x in range (0, DataRowNum):
			for z in range (0,K):
				# D[x][z] = cosine_similarity(P[x], C[z])
				D[x][z] = np.linalg.norm(np.array(P[x]) - np.array(C[z]))


		centroid_per_doc = []
		for x in range (0, DataRowNum):
			DISTTOCOMPARE = D[x]
			MINDIST = DISTTOCOMPARE.index(min(DISTTOCOMPARE))
			centroid_per_doc.append(MINDIST)
			CG[x] = MINDIST
			# print DISTTOCOMPARE
			# print MINDIST
			G[x][MINDIST] = 1
			TMPATTRC[MINDIST] = map(sum, zip(TMPATTRC[MINDIST],P[x]))
			# print 'P[',str(x),'] = ', P[x]
			# print 'TMPATTRC[',str(MINDIST),'] = ', TMPATTRC[MINDIST]

			CNTMEMBERC[MINDIST] += 1
		# print centroid_per_doc
		for z in range(0, K):
			if CNTMEMBERC[z] > 0:
				C_TEMP = 0.0
				C_ATTR_LIST = []
				for v in TMPATTRC[z]:
					C_TEMP = float(v)/float(CNTMEMBERC[z])
					C_ATTR_LIST.append(C_TEMP)
					# print "v", v, "CNTMEMBERC[z]", CNTMEMBERC[z], "v/CNTMEMBERC[z]", float(v)/float(CNTMEMBERC[z])
				C[z] = C_ATTR_LIST
					# print "G ", G
		if np.array_equal(G,GTEMP):
			# has_converged = True
			break
			

		GTEMP = G
		for k in range(0,K):
			print "cluster #", k, centroid_per_doc.count(k)
		print "Iteration #", i

	return [C, centroid_per_doc]

def Populate_Cluster():
	cluster_result_list = open('f_cluster_result')
	cluster_result = cluster_result_list.read()

	cluster_population = []
	for cr in cluster_result[:-1].split("\n"):
		population = []
		cluster = cr[:-1].split("-")
		cluster_index = cluster[0]
		if len(cluster) > 1:
			cluster_members = cluster[1].split(",")

			for member in cluster_members:
				member_index = int(member) - 1
				population.append(member_index)
			cluster_population.append(population)
	return cluster_population
def Populate_Distance(P):
	distance_matrix_file = open('f_distance_matrix','w+')
	distance_matrix = []
	numdoc = len(P)
	for x in range(0, numdoc):
		distance_from_x = []
		doc_index = ""
		for y in range(0, numdoc):
			dist =np.linalg.norm(np.array(P[x]) - np.array(P[y])) 
			distance_from_x.append(dist)
			doc_index += str(dist) + ","
		distance_matrix_file.write(doc_index[:-1]+"\n")
		distance_matrix.append(distance_from_x)
	distance_matrix_file.close()
	return distance_matrix
def Silhouette(P):
	#=========================================================================#
	#	Adopted from P.J. Rousseeuw 's Paper Silhouette Fx (1986)
	#	Code written by Irfan Wahyudin and Hermawan Wiryana
	#	Feel free to adopt this code, but... please kindly mention us...
	#=========================================================================#
	cluster_population = Populate_Cluster()
	c = 0
	s = 0.0
	c1 = 0 
	c2 = 0
	s_list = []
	s_list_all = []
	sum_s = 0.0
	iters = 0
	D = []
	distance_matrix_file = open('f_distance_matrix')
	distance_matrix = distance_matrix_file.read()

	for doc in distance_matrix.split("\n"):
		item_dist = []
		for dist in doc.split(","):
			item_dist.append(dist)
		D.append(item_dist)
	for curr_cluster in cluster_population:
		s_list = []
		ac = 0
		num_population = float(len(curr_cluster))
		for i in curr_cluster:
			a = 0.0
			for member in cluster_population[c1]:
				if member != i:
					# a += abs(np.linalg.norm(np.array(D[member]) - np.array(D[i])))
					try:
						a += float(D[member][i])
					except:
						print "member", member, "i",i
						return
			a = float(a) / float(num_population) #Count Average

			c2 = 0
			num_population_neigh = 0
			b_list = []
			b_temp = 0.0
			for neigh_cluster in cluster_population:
				num_population_neigh = 0
				b_temp = 0.0
				if c2 != c1:
					for member in neigh_cluster:
						# b_temp += abs(np.linalg.norm(np.array(D[member]) - np.array(D[i])))
						b_temp += float(D[member][i])
						num_population_neigh+=1
					b_temp = float(b_temp) / float(num_population_neigh) #Count Average
					b_list.append(b_temp)
				c2+=1

			b = min(b_list)
			# print "a", a,"b", b
			if max(b,a) == 0:
				s = 0.0
			else:
				s = (b - a) / max(b,a)
			# print "s = ", s
			s_list.append(s)
			sum_s += s
			iters+=1
			print "s", s
		s_list_all.append(reduce(lambda x, y: x + y,s_list) / len(s_list))
		c1+=1
	print "sum_s",sum_s, sum_s / float(iters)
	return s_list_all

# P = [[10,26,31,446],
# 	 [8,28,28,342],	
# 	 [7,25,16,266],
# 	 [9,25,21,249],
# 	 [9,27,42,213],
# 	 [3,24,37,419],
# 	 [3,29,43,238],
# 	 [5,24,37,438],
# 	 [8,32,21,348],
# 	 [10,24,12,279],
# 	 [8,28,28,342]]

# K_Means(3, P)

