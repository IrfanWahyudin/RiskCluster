kamus_file = ""
kamus = []
kata_dasar = ""
def BacaKamus():
	global kamus
	kamus_file = open("kamus.txt")
	kamus = str(kamus_file.read()).split(" ")

def CekKamus(kata):
	try:
		index = kamus.index(kata)
		if index > 0: return True
		else: return False
	except:
		return False
def KataDasar(kata):
	kata_olah1 = ""
	kata_olah2 = ""
	kata_olah3 = ""
	BacaKamus()
	kata_olah1 = HapusInflectionSuffixes(kata)
	akhiran, kata_olah2 = HapusDerivationSuffixes(kata_olah1)
	kata_olah3 = HapusDerivationPrefix(akhiran, kata_olah2, kata)

	if CekKamus(kata_olah1):
		return kata_olah2
	elif CekKamus(kata_olah2):
		return kata_olah2
	elif CekKamus(kata_olah3):
		return kata_olah3

	if kata_olah3=="" or kata_olah3==None:
		if kata_olah2=="":
			if kata_olah1=="" or kata_olah2==None:
				return kata
			else:
				return kata_olah1
		else:
			return kata_olah2
	else:
		return kata_olah3


def HapusInflectionSuffixes(kata):
	if kata.endswith("lah") or kata.endswith("kah") or kata.endswith("nya"):
		return left(kata,len(kata) - 3)
	elif kata.endswith("mu") or kata.endswith("ku"):
		return left(kata,len(kata) - 2)
	elif kata.endswith("lah") or kata.endswith("kah") or kata.endswith("tah") or kata.endswith("pun"):
		kata_olah1 = left(kata,len(kata) - 3)
		kata_olah2 = HapusInflectionSuffixes(kata_olah1)
		return kata_olah2
	else:
		return kata

def HapusDerivationSuffixes(kata):
	akhiran = ""
	kata_olah1 = ""
	kata_olah2 = ""


	if kata.endswith("i"):
		kata_olah1 = mid(kata,0,len(kata)-1)
		akhiran = "i"
	elif kata.endswith("an"):
		kata_olah1 = mid(kata,0,len(kata)-2)
		akhiran = "an"
	elif kata.endswith("kan"):
		kata_olah1 = mid(kata,0,len(kata)-3)
		akhiran = "kan"


	if CekKamus(kata_olah1):		
		return akhiran,kata_olah1
	else:
		if kata_olah1.endswith("k"):

			kata_olah2 = mid(kata,0,len(kata_olah1)-1)
			if CekKamus(kata_olah2):
				return akhiran,kata_olah2
			else:
				return akhiran,kata_olah2
		else:

			if kata_olah1 != "":
				kata_olah2 = kata_olah1
			else:
				kata_olah2 = kata

	return akhiran,kata_olah2

def HapusDerivationPrefix(akhiran, kata_olah2, kata):
	ketemu = False
	kata_olah3 = ""
	if akhiran != "":
		if kata_olah2.startswith("be") and kata_olah2.endswith("i"):
			ketemu = CekKamus(kata_olah2)
		elif (kata_olah2.startswith("di") or kata_olah2.startswith("me")) and kata_olah2.endswith("an"):
			ketemu = CekKamus(kata_olah2)
		elif (kata_olah2.startswith("ke") or kata_olah2.startswith("se") ) and (kata_olah2.endswith("i") or kata_olah2.endswith("kan")):
			ketemu = CekKamus(kata_olah2)

	if ketemu:
		return kata_olah2
	else:
		if kata_olah2.startswith("ke"):
			return mid(kata_olah2,2,len(kata_olah2))
		if kata_olah2.startswith("se"):
			return mid(kata_olah2,2,len(kata_olah2))
		if kata_olah2.startswith("pe") or kata_olah2.startswith("dipe"):
			kata_olah3 = mid(kata_olah2,2,len(kata_olah2))
			
			if CekKamus(kata_olah3):
				return kata_olah3	
			else:
				if kata_olah2.startswith("pen"):
					kata_olah3 = mid(kata_olah2,3,len(kata_olah2))

					if CekKamus(kata_olah3):
						return kata_olah3
					else:
						if CekKamus("t" + kata_olah3):
							return "t" + kata_olah3
						if kata_olah2.startswith("peny"):	
							kata_olah3 = mid(kata_olah2,4,len(kata_olah2))
							
							if CekKamus("s" + kata_olah3):
								return "s" + kata_olah3
							else:
								return "s" + kata_olah3
				elif kata_olah2.startswith("per") or kata_olah2.startswith("diper"):
					if kata_olah2.startswith("per"):
						kata_olah3 = mid(kata_olah2,3,len(kata_olah2))

						if CekKamus(kata_olah3):
							return kata_olah3
						else:
							return kata_olah3
					elif kata_olah2.startswith("diper"):
						kata_olah3 = mid(kata_olah2,5,len(kata_olah2))

						if CekKamus(kata_olah3):
							return kata_olah3
						else:
							return kata_olah3
				elif kata_olah2.startswith("pem"):
					kata_olah3 = mid(kata_olah2,3,len(kata_olah2))

					if CekKamus(kata_olah3):
						return kata_olah3
					else:
						if CekKamus("p" + kata_olah3):
							return "p" + kata_olah3
						else:
							return "p" + kata_olah3
		if kata_olah2.startswith("me"):
			kata_olah3 = mid(kata_olah2,2,len(kata_olah2))

			if CekKamus(kata_olah3):
				# if (kata_olah3.startswith("l") or kata_olah3.startswith("m") or kata_olah3.startswith("n") or kata_olah3.startswith("r") or kata_olah3.startswith("w")):
				return kata_olah3	
			else:
				if kata_olah2.startswith("meng"):
					
					kata_olah3 = mid(kata_olah2,4,len(kata_olah2))
					
					if CekKamus(kata_olah3):				
						return kata_olah3
					else:
						if CekKamus("g" + kata_olah3):
							return "g" + kata_olah3
						elif CekKamus("h" + kata_olah3):
							return "h" + kata_olah3
						elif CekKamus("k" + kata_olah3):
							return "k" + kata_olah3 
				elif kata_olah2.startswith("mem"):
					kata_olah3 = mid(kata_olah2,3,len(kata_olah2))

					if CekKamus(kata_olah3):				
						return kata_olah3
					else:
						if CekKamus("p" + kata_olah3):
							return "p" + kata_olah3
						else:
							return "p" + kata_olah3
					return kata_olah3
				elif kata_olah2.startswith("men"):
					kata_olah3 = mid(kata_olah2,3,len(kata_olah2))
					if CekKamus(kata_olah3):				
						return kata_olah3
					else:
						if CekKamus("t" + kata_olah3):
							return "t" + kata_olah3							
						if kata_olah2.startswith("meny"):
							kata_olah3 = mid(kata_olah2,4,len(kata_olah2))

							if CekKamus("s" + kata_olah3):
								return "s" + kata_olah3

					return kata_olah3
		if kata_olah2.startswith("ber"):
			kata_olah3 = mid(kata_olah2,3,len(kata_olah2))
			if CekKamus(kata_olah3):
				return kata_olah3

				

	return kata_olah3



def vowel(huruf):
	if (huruf == 'a' or huruf == 'i' or huruf == 'u' or huruf == 'e' or huruf == 'o'):
		return True
	else:
		return False

def left(s, amount):
	#left
    return s[:amount]

def right(s, amount):
	#right
    return s[-amount:]

def mid(s, offset, amount):
	#mid
    return s[offset:offset+amount]
# print KataDasar("mengadopsi")