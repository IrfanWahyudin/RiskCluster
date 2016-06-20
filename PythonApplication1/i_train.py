import i_k_means as km
import i_preprocess as p
import i_lsi as l
import i_sse as sse
import time

def write_result(C, CR):
	cf = open('f_centroids', 'w+')
	for k in C:
		c_value_str = ""
		for c_value in k:
			c_value_str+=str(c_value)+" "
		cf.write(c_value_str+";")
	cf.close()

	cluster_result = open("f_cluster_result", "w+")
	for cluster in range(K):
		cluster_result.write(str(cluster) + "-")
		for indeks,value in enumerate(CR):
			if value == cluster:
				cluster_result.write(str(indeks+1) + ",")
				# print [str(indeks+1)] 
		cluster_result.write("\n")

	cluster_result.close()

#========================================================================#
#						Load Text as Observation Data
#========================================================================#
D = p.do_the_magic()
# p.preprocess(len(D),D)
# p.Weighting()
numdoc = len(D)
tfidfreturn = p.do_tfidf(numdoc, D)
bowt = open('f_bag_of_weighted_terms','w+')

bag_of_weighted_terms = tfidfreturn

for d in bag_of_weighted_terms:
	for wt in d:
		bowt.write(str(wt).rstrip().lstrip() + ",")
	bowt.write("\n")
bowt.close()


# P = tfidfreturn
#========================================================================#
#========================================================================#
#						Load Iris as Observation Data
#========================================================================#
# f = open('iris','r')
# f_iris = f.read().split('\n')
# f.close()

# iris = [[float(v) for v in i.split(',')] for i in f_iris]
# P = iris
# tfidfreturn = P

#========================================================================#
#========================================================================#
#						Load SVD as Observation Data
#========================================================================#
# P = l.main("")
# # print "dim", len(P)
# tfidfreturn = P
# f = open('f_bag_of_weighted_terms_svd','w+')
# for row in P:
# 	for col in row:
# 		f.write(str(col) + ",")
# 	f.write("\n")
# f.close()
#========================================================================#


Means = 2

K = 6
alpha = 0.9
beta = 0.9
start_time = time.time()
		
while (K<=10):
	while (alpha<1.0):
		while (beta<1.0):
			print "alpha", alpha, "beta",beta,"K",K
			fs = open('f_silhouette','a')
			try:
				start_time = time.time()
				#=============================================#
				#	Check for all distance between objects
				#=============================================#
				dist_matrix_file = open("f_distance_matrix")
				dist_matrix = dist_matrix_file.read()
				# print "Jumlah dokumen", len(D)
				# print "Jumlah dokumen", len(tfidfreturn)
				if dist_matrix == "":
					print "f_distance_matrix Empty..."
					print "Measure all distances between objects..."
					km.Populate_Distance(tfidfreturn)
					print "Measure all distances done..."
				dist_matrix_file.close()
				#=============================================#
				C, CR = km.K_Means(K,P,Means,alpha, beta)
				if C!= 0.0:
					write_result(C, CR)
					s_overall = []
					s_current = km.Silhouette(P)
					s_overall.append(reduce(lambda x, y: float(x) + float(y),s_current) / len(s_current))
					
					print "S =",s_overall

					fs.write(str(K) + "--" + str(alpha) + "--" + str(beta) + "--s_overall=" + str(s_overall) + "--s_current=" + str(s_current)+ "\n")
					sse.compute_sse(K, alpha, beta)
				elapsed_time = time.time() - start_time	

				print "elapsed time : ", elapsed_time
				start_time = time.time()
				exit
			except:
				fs.write(str(K) + "--" + str(alpha) + "--" + str(beta) + "Not Feasible" + "\n")
				print "Exception...Not feasible..."
				elapsed_time = time.time() - start_time	

				print "elapsed time : ", elapsed_time
				beta+=0.05
				if int(beta)>=1:
					beta=0.5
				continue
			fs.close()
			
			beta+=0.05
		if int(beta)>=1:
			beta=0.5

		alpha+=0.05
	if int(alpha)>=1:
		alpha=0.4
	K+=1
# your code
elapsed_time = time.time() - start_time	

print "elapsed time : ", elapsed_time