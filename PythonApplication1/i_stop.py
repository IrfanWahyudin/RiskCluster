from nltk.corpus import stopwords

tweet = "saya tidak percaya telkomsel bagus"

for t in tweet.split(' '):
	if t not in stopwords.words('indonesian'):
		print t