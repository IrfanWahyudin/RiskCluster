import sqlite3 as sql3
import distance
import hmm_tagger as ht
import codecs

swn_dict = "swn_dict/"
swn_id_db = {}
swn_en_db = {}
swn_db = {}
word_id = {}
word_en = {}
alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
tags = ['v','n','r','a']

for alphabet in alphabets:
	for tag in tags:
		swn_id_db[alphabet+tag] = []
		swn_en_db[alphabet+tag] = []
		swn_db[alphabet] = []

def peb_tag(word):
	splitted_word = []
	splitted_word = word.split("/")
	return splitted_word
def swn_tag(pos_tag):	
	if (pos_tag == "VB" or pos_tag == "VBD" or pos_tag == "VBT" or pos_tag == "VBG" or pos_tag == "VBN" or 
		pos_tag == "VBP" or pos_tag == "VBZ" or pos_tag == "VBI"):
		return "v"
	elif (pos_tag == "NN" or pos_tag == "NNS" or pos_tag == "NNP" or pos_tag == "NNPS"):
		return "n"
	elif (pos_tag == "RB" or pos_tag == "RBR" or pos_tag == "RBS"):
		return "r"
	elif (pos_tag == "JJ" or pos_tag == "JJR" or pos_tag == "JJS"):
		return "a"
	else:
		return "a"
def insert_swn_id():
	conn = sql3.connect('DB_WORDS')
	c = conn.cursor()
	i = 0
	with open('DB_WORDS.sql') as fp:
	    for line in fp:
	        c.execute(line)
	        if i % 10000 == 0:
	        	conn.commit()
	        	print i
	        i+=1

	print "DONE!!!"

	conn.close()
	fp.close()

def fill_swn():
	i = 0
	for alphabet in alphabets:
		for tag in tags:
			f = open(swn_dict + alphabet, "r")
			swn_id = f.read()

			for line in swn_id.split("\n"):
				swn = line.split(",")
				if swn[0]!="":
					swn_db[alphabet].append([swn[0],swn[1],swn[2],swn[3],swn[4]])
				
			f.close()
def fill_swn_id():
	i = 0
	for alphabet in alphabets:
		for tag in tags:
			f = open(swn_dict + alphabet + tag + "_id", "r")
			swn_id = f.read()

			for line in swn_id.split("\n"):
				swn = line.split(",")
				if swn[0]!="":
					swn_id_db[alphabet + tag].append([swn[0],swn[1],swn[2],swn[3],swn[4]])
				
			f.close()
def fill_swn_en():
	for alphabet in alphabets:
		for tag in tags:
			f = codecs.open(swn_dict + alphabet + tag + "_en", "r",encoding='utf-8')
			swn_en = f.read()

			for line in swn_en.split("\n"):
				swn = line.split(",")
				if swn[0]!="":
					swn_en_db[alphabet + tag].append([swn[0],swn[1],swn[2],swn[3],swn[4]])
				
			f.close()
def retrieve_swn():
	conn = sql3.connect('DB_WORDS')	
	swn = []
	c = conn.cursor()
	for alphabet in alphabets:
		f = codecs.open(swn_dict + alphabet, "w+",encoding='utf-8')
		select = "select lower(word_id) as word_id,word_type,avg(pos), avg(neg), 1-abs(avg(pos)-avg(neg)) as obj from "
		where_condition = " (select lower(word_id) as word_id,word_type,pos, neg from ref_sentiwordnet_nodesc   "
		where_condition += "	where word_id is not null and substr(word_id,1,1) ='" + alphabet + "')"
		order_by = " group by lower(word_id), word_type order by lower(word_id) asc"
		sql = select + where_condition + order_by
		print sql
		rows = c.execute(sql)
		print "adding ", alphabet
		for row in rows:			
			f.write(row[0]+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+"\n")
			swn_db[alphabet].append(row)
		f.close()
def retrieve_swn_id():
	global swn_dict
	conn = sql3.connect('DB_WORDS')
	
	swn = []
	c = conn.cursor()
	for alphabet in alphabets:
		for tag in tags:
			f = codecs.open(swn_dict + alphabet + tag + "_id", "w+",encoding='utf-8')
			select = "select lower(word_id) as word_id,word_type,avg(pos), avg(neg), 1-abs(avg(pos)-avg(neg)) as obj from "
			where_condition = " (select lower(word_id) as word_id,word_type,pos, neg from ref_sentiwordnet_nodesc "
			where_condition += "	where word_id is not null and substr(word_id,1,1) ='" + alphabet + "' and word_type = '" + tag + "')"
			order_by = " group by lower(word_id), word_type order by lower(word_id) asc"
			sql = select + where_condition + order_by

			rows = c.execute(sql)
			print "adding ", alphabet + tag
			for row in rows:			
				f.write(row[0]+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+"\n")
				swn_id_db[alphabet + tag].append(row)
			f.close()
def retrieve_swn_en():
	conn = sql3.connect('DB_WORDS')	
	swn = []
	c = conn.cursor()
	for alphabet in alphabets:
		for tag in tags:
			f = codecs.open(swn_dict + alphabet + tag + "_en", "w+",encoding='utf-8')
			select = "select lower(word_en) as word_en,word_type,avg(pos), avg(neg), 1-abs(avg(pos)-avg(neg)) as obj from "
			where_condition = " (select lower(word_en) as word_en,word_type,pos, neg from ref_sentiwordnet_nodesc "
			where_condition += "	where word_en is not null and substr(word_en,1,1) ='" + alphabet + "' and word_type = '" + tag + "')"
			order_by = " group by lower(word_en), word_type order by lower(word_en) asc"
			sql = select + where_condition + order_by

			rows = c.execute(sql)
			print "adding ", alphabet + tag
			for row in rows:			
				f.write(row[0]+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+"\n")
				swn_en_db[alphabet + tag].append(row)
			f.close()

def word_weighting(kata):
	pos = 0.0
	neg = 0.0
	obj = 0.0
	pos_id = 0.0
	neg_id = 0.0
	obj_id = 0.0
	pos_en = 0.0
	neg_en = 0.0
	obj_en = 0.0
	splitted_word = kata.split("|") 
	theword = splitted_word[0]
	swntag =splitted_word[1]  #get swn tag
	nearest_word = ""
	word_index = ""
	min_distance = 999999999999999
	min_distance_id = 999999999999999
	min_distance_en = 999999999999999
	curr_distance = 0
	curr_distance_id = 0
	curr_distance_en = 0
	nearest_word_id = ""
	nearest_word_en = ""
	first_letter = left(theword,1)
	if first_letter in alphabets and swntag in tags:
		print "Looking for ", theword , "------------------"
		for swn_id in swn_id_db[first_letter+swntag]:
			swn_word = swn_id[0]
			the_word = theword.encode('utf-8')
			curr_distance_id = distance.levenshtein(swn_word.lower(), the_word.lower())
			# print 'swn_id[0]', swn_id[0], 'curr_distance', curr_distance_id
			if curr_distance_id < min_distance_id:
				min_distance_id = curr_distance_id
				nearest_word_id = swn_id[0]	
				pos_id = swn_id[2]
				neg_id = swn_id[3]
				obj_id = swn_id[4]
				# word_index = swn_id[1]
				if curr_distance_id == 0: break
		
		if curr_distance_id > 0:
			print "Bad search, search in english db"
			for swn_en in swn_en_db[first_letter+swntag]:
				swn_word = str(swn_en[0]).encode('utf-8')
				the_word = theword.encode('utf-8')
				curr_distance_en = distance.levenshtein(swn_word.lower(), the_word.lower())
				if curr_distance_en < min_distance_en:
					min_distance_en = curr_distance_en
					nearest_word_en = swn_en[0]	
					pos_en = swn_en[2]
					neg_en = swn_en[3]
					obj_en = swn_en[4]
					# word_index = swn_en[1]
					if curr_distance_en == 0: break

		print min_distance_id, min_distance_en
		if min_distance_id <= min_distance_en:
			pos = pos_id
			neg = neg_id
			obj = obj_id
			min_distance = min_distance_id
			nearest_word = nearest_word_id
		else:
			pos = pos_en
			neg = neg_en
			obj = obj_en
			min_distance = min_distance_en
			nearest_word = nearest_word_en
		print nearest_word,  " min_distance = ", min_distance," pos = ", pos, " neg = ", neg, " obj =", obj
	else:
		print "Looking for ", theword , "------------------"
		for swn_id in swn_db[first_letter]:
			swn_word = swn_id[0]
			the_word = theword.encode('utf-8')
			curr_distance_id = distance.levenshtein(swn_word.lower(), the_word.lower())
			# print 'swn_id[0]', swn_id[0], 'curr_distance', curr_distance_id
			if curr_distance_id < min_distance_id:
				min_distance_id = curr_distance_id
				nearest_word_id = swn_id[0]	
				pos_id = swn_id[2]
				neg_id = swn_id[3]
				obj_id = swn_id[4]
				# word_index = swn_id[1]
				if curr_distance_id == 0: break
	# if pos>neg:
	# 	return pos
	# elif neg>pos:
	# 	return -1*neg
	# elif pos==neg:
	# 	return 1
	return [nearest_word, min_distance, pos, neg, obj]
		

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

# retrieve_swn_id()
# retrieve_swn_en()
# retrieve_swn()
fill_swn()
fill_swn_id()
fill_swn_en()






