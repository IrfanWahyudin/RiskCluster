from __future__ import division
import Orange
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import math
import operator
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot
# table = Orange.data.Table("iris")

num_of_reseptor = 10
data = [random.random for i in range (0,num_of_reseptor)]
num_of_cell = 5
cell = [data] * num_of_cell

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
			DistanceToCompare = D[x]
			MinimumDistance = DistanceToCompare.index(min(DistanceToCompare))
			CG[x] = MinimumDistance
			# print DistanceToCompare
			# print MinimumDistance
			G[x][MinimumDistance] = 1
			TMPATTRC[MinimumDistance] = map(sum, zip(TMPATTRC[MinimumDistance],P[x])) 
			# print 'P[',str(x),'] = ', P[x]
			# print 'TMPATTRC[',str(MinimumDistance),'] = ', TMPATTRC[MinimumDistance]
			
			CNTMEMBERC[MinimumDistance] += 1

		for z in range(0, K):
			if CNTMEMBERC[z] > 0:
				C[z][:] = [v / CNTMEMBERC[z] for v in C[z]]

		# print "G ", G
		# print "GTEMP ", GTEMP
		if np.array_equal(G,GTEMP):
			break
		
	 	GTEMP = G

	print "Iteration ", i
	# assignment = np.array(CG)
	# Pnp = np.array(P)
	# fig = plt.figure(1)
	# ax = Axes3D(fig)

	# ax.scatter(Pnp[:,0],Pnp[:,1],Pnp[:,2], Pnp[:,3], c=assignment)
	#pyplot.scatter(P[0], P[1], P[2], P[3], c=assignment)
	# plt.show()


def generate_population():
    init_cell = [] * num_of_cell
    cell = [] * num_of_cell
    valrange = 100000
    for i in range(0,num_of_cell):
        val = random.sample(xrange(valrange), num_of_reseptor) 
        
        init_cell.append([x / valrange for x in val],)

    cell =  init_cell

    print cell
            

    

#voting = Orange.data.Table("voting")
#kmeans(voting)

generate_population()
