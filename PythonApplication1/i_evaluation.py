import matplotlib.pyplot as plt
import numpy as np
def evaluate(fld1, fld2):
	f = open('f_cluster_result')
	cluster_result = f.read().split('\n')
	f.close()

	f = open('f_bag_of_weighted_terms')
	weighted_terms = f.read().split('\n')
	f.close()

	f = open('f_wordlist')
	wordlist = f.read().split('\n')
	f.close()

	bag_of_weighted_terms = []
	member_list = []

	for wt in weighted_terms:
		bag_of_weighted_terms.append([[i, float(x)] for i, x in enumerate(wt[:-1].split(',')) if x != ''])

	f = open('f_cluster_words','w')		
	top = 200

	stopwords_extension = [0, 1, 5, 7, 87, 9, 17, 29, 38, 50, 72, 97, 125, 221, 222 ,305, 311] 
	for c, cluster in enumerate(cluster_result):
		cluster_risk = 0.0
		cluster = cluster.split('-')
		pos_wordlist = [[i,0] for i in range(0,len(wordlist))]
		if len(cluster)>1:
			members = [int(x)-1 for x in cluster[1].split(',') if x != '']

			for member in members:
				try:
					sorted_words =  bag_of_weighted_terms[member-1]#sorted(bag_of_weighted_terms[member-1], key=lambda x: x[1], reverse=False)
					member_list.append([sorted_words[fld1][1],sorted_words[fld2][1], c])
					for sw in sorted_words:				
						if float(sw[1]) != 0.0 and sw[0] not in stopwords_extension:
							pos_wordlist[sw[0]][1]+=1	
							if float(sw[1]) < 0.0:					
								cluster_risk += sw[1]
				except:
					print i, member
					
		sorted_pos_wordlist = sorted(pos_wordlist, key=lambda x: x[1], reverse=True)
		print sorted_pos_wordlist[:top]


		for spw in sorted_pos_wordlist[:top]:
			theword = wordlist[spw[0]]
			# print theword
			f.write(theword + ',')
		f.write('|' + str(cluster_risk) + '|' + str(len(members)))
		print c
		f.write('\n')
	f.close()
	return member_list, bag_of_weighted_terms

def get_color_shape(c):
	if c == 0:
		return 'bs'
	elif c == 1:
		return 'g*'
	elif c == 2:
		return 'rh'
	elif c == 3:
		return 'cH'
	elif c == 4:
		return 'm+'
	elif c == 5:
		return 'kx'
	elif c == 6:
		return 'yd'
	elif c == 7:
		return 'kp'
f = open('f_centroids')
centroids = f.read().split(';')
f.close()

fld1 = 8 
fld2 = 7 
centroids_list = []
for centroid in centroids[:-1]:
	c = centroid.lstrip().rstrip().split(' ')
	centroids_list.append([float(c[fld1]), float(c[fld2])])

print centroids_list
# plt.plot(centroids_list[0][0],centroids_list[0][1],centroids_list[1][0],centroids_list[1][1],centroids_list[2][0],centroids_list[2][1],centroids_list[3][0],centroids_list[3][1],centroids_list[4][0],centroids_list[4][1],centroids_list[5][0],centroids_list[5][1],centroids_list[6][0],centroids_list[6][1],centroids_list[7][0],centroids_list[7][1])

member_list = evaluate(fld1, fld2)
# for c, cl in enumerate(centroids_list):
# 	cs = get_color_shape(c)
# 	plt.plot(cl[0],cl[1],cs)

# for ml in member_list:
# 	cs = get_color_shape(ml[2])
# 	plt.plot(ml[0],ml[1],cs)	

# print len(member_list)
# plt.show()
	



