# c = [1,2,3,4,5,6,6,7]
# l = [1,1,2,1,1,3,1,5,5,4,1,2,2]
# print [l for l in c]
# # print [[str(indeks) for indeks,value in enumerate(l) if value == cluster] for cluster in c]

# # for cluster in c:
# # 	print [str(indeks) for indeks,value in enumerate(l) if value == cluster] 

# # s = "33.123123124124  "
# # f = float(s)
# # print f

# cluster_result_list = open('cluster_result')
# cluster_result = cluster_result_list.read()

# cluster_population = []
# for cr in cluster_result[:-1].split("\n"):
# 	population = []
# 	cluster = cr[:-1].split("-")
# 	cluster_index = cluster[0]
# 	cluster_members = cluster[1].split(",")

# 	for member in cluster_members:
# 		member_index = int(member) - 1
# 		population.append(member_index)
# 	cluster_population.append(population)

# print cluster_population

# c = 0
# s = 0.0
# c1 = 0 
# c2 = 0
# s_list = []
# s_list_all = []
# for curr_cluster in cluster_population:
# 	ac = 0
# 	num_population = float(len(curr_cluster))
# 	for i in curr_cluster:
# 		a = 0.0
# 		for member in cluster_population[c1]:
# 			if member != i:
# 				a += abs(member - i)
# 		a = float(a) / float(num_population) #Count Average

# 		cx = 0
# 		cnt_member = 0
# 		b_list = []
# 		b_temp = 0.0
# 		for neigh_cluster in cluster_population:
# 			cnt_member = 0
# 			if c2 != c1:
# 				for member in neigh_cluster:
# 					b_temp += abs(member - i)
# 					cnt_member+=1
# 				b_temp = float(b_temp) / float(cnt_member)
# 				b_list.append(b_temp)
# 			c2+=1
		

# 		b = min(b_list)

# 		s = (b - a) / max(b,a)
# 		print "s", s
# 	s_list.append(s)
# 	s_list_all.append(reduce(lambda x, y: float(x) + float(y),s_list) / len(s_list))
# 	c1+=1

# print s_list_all
#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# import locale
# import os
# import sys
# import unicodedata


# xyz = [1,2,1,3,1,3,1,1,2,2,2]
# wa = "\xe9"
# print wa.encode('utf8','replace')


# print sw.word_weighting("benchmark|n")
# f1 = open('f_wordlist','r')
# f_wordlist = f1.read().split("\n")
# f1.close()

# f2 = open('f_wordlist_weighted','r')
# f_wordlist_weighted = f2.read().split("\n")
# f2.close()
# print f_wordlist_weighted[f_wordlist.index("musa|n")].split("|")


# fs = open('f_silhouette','w+')
# while (K<11):
# 	while (alpha<1.0):
# 		while (beta<1.0):
# 			beta+=0.05
# 			fs.write(str(K) + "--" + str(alpha) + "--" + str(beta) + "\n")
	
# 		if int(beta)==1:
# 			beta=0.1

# 		alpha+=0.05

# 	if int(alpha)==1:
# 		alpha=0.1
# 	K+=1
# fs.close()
# P = [[1,1,2,1],[1,3,1,5],[5,4,1,2]]

# temp = [0,0,0,0]
# for p in P:
# 	temp = [x + y for x, y in zip(temp, p)]

# M = [float(x)/float(len(P)) for x in temp]

# SE = 0.0
# for p in P:
# 	SE =[(x - y)**2 for x, y in zip(p, M)]


# print sum(SE)
# import i_k_means as k 
# K = 3

# f = open('iris','r')
# f_iris = f.read().split('\n')
# f.close()

# iris = [[float(v) for v in i.split(',')] for i in f_iris]
# print iris
# CMethod = 2
# k.Populate_Distance(iris)
# k.K_Means(K, iris, CMethod, aplha = 0.25, beta = 0.33 )
# print k.Silhouette(iris)
# import numpy as np
# f = open('f_centroids','r')
# f_centroids = f.read()
# f.close()

# f = open('f_cluster_result')
# f_cluster_result = f.read().split('\n')
# f.close()

# f = open('f_bag_of_weighted_terms_svd')
# f_bag_of_weighted_terms_svd = f.read().split('\n')
# f.close()

# centroid = []
# bag_of_weighted_terms_svd = []
# SSE = []
# total_SSE = 0.0
# for b in f_bag_of_weighted_terms_svd:
# 	bag_of_weighted_terms_svd.append([float(item) for item in b.split(',') if item != '' ])


# for c in f_centroids.split(';')[:-1]:
# 	centroid.append([float(item) for item in c.split(' ') if item != '' ])

# for c, cluster in enumerate(f_cluster_result[:-1]):
# 	cluster = cluster.split('-')
# 	curr_SSE = 0.0
# 	if len(cluster)>1:		
# 		members = [int(x)-1 for x in cluster[1].split(',') if x != '']
		
# 		for member in members:
# 			per_member_SSE = 0.0
# 			for i,item in enumerate(bag_of_weighted_terms_svd[member]):
# 				# print "SSE", member, c, (item - centroid[c][i]) ** 2
# 				curr_SSE += (item - centroid[c][i]) ** 2
# 				per_member_SSE += (item - centroid[c][i]) ** 2
# 			print c, member, i, curr_SSE, per_member_SSE

# 	if len(members) == 0:
# 		SSE.append(-1.0)
# 	else:
# 		SSE.append(curr_SSE / len(members))
# 	total_SSE += curr_SSE
# print total_SSE, c, total_SSE / c
# print SSE

x = [1,2,3,4,5]
f = open('f_sse','w+')
for y in x:
	f.write(str(y))
f.close()