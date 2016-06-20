import numpy as np
def compute_sse(k, alpha, beta):
	f = open('f_centroids','r')
	f_centroids = f.read()
	f.close()

	f = open('f_cluster_result')
	f_cluster_result = f.read().split('\n')
	f.close()

	f = open('f_bag_of_weighted_terms_svd')
	f_bag_of_weighted_terms_svd = f.read().split('\n')
	f.close()

	centroid = []
	bag_of_weighted_terms_svd = []
	SSE = []
	total_SSE = 0.0
	for b in f_bag_of_weighted_terms_svd:
		bag_of_weighted_terms_svd.append([float(item) for item in b.split(',') if item != '' ])


	for c in f_centroids.split(';')[:-1]:
		centroid.append([float(item) for item in c.split(' ') if item != '' ])

	for c, cluster in enumerate(f_cluster_result[:-1]):
		cluster = cluster.split('-')
		curr_SSE = 0.0
		if len(cluster)>1:		
			members = [int(x)-1 for x in cluster[1].split(',') if x != '']
			
			for member in members:
				per_member_SSE = 0.0
				for i,item in enumerate(bag_of_weighted_terms_svd[member]):
					# print "SSE", member, c, (item - centroid[c][i]) ** 2
					curr_SSE += (item - centroid[c][i]) ** 2
					per_member_SSE += (item - centroid[c][i]) ** 2
				print c, member, i, curr_SSE, per_member_SSE

		if len(members) == 0:
			SSE.append(-1.0)
		else:
			SSE.append(curr_SSE / len(members))
		total_SSE += curr_SSE
		if c>0.0:
			# print total_SSE, c, total_SSE / c
			# print SSE
			f = open('f_sse','a')
			f.write(str(k) + "," + str(alpha) + "," + str(beta) + ",")
			for e in SSE:
				f.write(str(e) + ",")
			f.write("\n")
			f.close()

compute_sse(6,0.9,0.9)
