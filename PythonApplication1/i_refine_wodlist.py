import i_sentiment_weighting as s 
import i_preprocess as p
import hmm_tagger
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

f = open('f_wordlist_refine')
wordlist_refine = f.read()
f.close()

for w in wordlist_refine.split("\n"):
	items = w.split("|")
	words = items[0]
	category = items[1]
	word_type = items[2]
	word_score = 0
	accumulate_score = 0
	default_score = items[3]
	if category == "UNK":
		word_type = "o"
	word_length = len(words.split(" "))

	nearest_word = words
	if category == "REM":
		word_score = 1
	elif category == "BKP":
		word_score = default_score
	else:
		if word_length == 1:
			nearest_word, min_distance, pos, neg, obj = s.word_weighting(words + "|" + word_type)
			if pos >= neg:
				word_score = 1
			else:
				word_score = -1
		else:
			tagged_sentence = hmm_tagger.do_tag(words)
			words_postag = tagged_sentence.split(" ")
			accumulate_score = 0
			accumulate_nearest_words = ""
			for wp in words_postag:
				the_word, peb_tag = p.peb_tag(wp)
				swn_tag = p.swn_tag(peb_tag)
				nearest_word, min_distance, pos, neg, obj = s.word_weighting(the_word + "|" + swn_tag)
				accumulate_nearest_words += " " + nearest_word
				if pos >= neg:
					accumulate_score +=1
				else:
					accumulate_score -=1
			if accumulate_score >= 0:
				word_score = 1
			else:
				word_score = -1
			nearest_word = accumulate_nearest_words

	f0 = open('f_wordlist_refine_fixed','a')
	f0.write(words + "|" + nearest_word + "|" + str(word_score		 ) + "\n")
	f0.close()




