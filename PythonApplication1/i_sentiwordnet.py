import json
import db_interpreter
import string_manipulation
import goslate
class sentiwordnet(object):
    """description of class"""
    def read_swn_english(self):
        o_dbinterpreter = db_interpreter.dbinterpreter()
        o_stringmanipulation = string_manipulation.stringmanipulation()
        path = 'C:\\Users\\irfan\\Documents\\Library\\Thesis\\Sentiwordnet\\home\\swn\\www\\admin\\dump\\'
        #file1 = 'SentiWordNet_3.0.0_20130122.txt'
        file1 = 'SentiWordNet.txt'
        file2 = 'SentiWordNet.json'
        lines = []
        data = ''
        with open(path + file1) as f:
            content = f.readlines()
            for line in content:
                attributes = line.split('\t')
                index = 0
                word_type = ''
                pos = 0.0
                neg = 0.0
                word = ''
                description = ''
                for attribute in attributes:
                    if index == 0:
                        word_type = attribute
                    elif index == 1:
                        word_index = attribute
                    elif index == 2:
                        pos = attribute
                    elif index == 3:
                        neg = attribute
                    elif index == 4:
                        words = attribute.split('#')
                        words_len = len(words)
                        if words_len > 2:
                            words_len = words_len                            
                        else:
                            word = words[0]
                    elif index == 5:
                        description = attribute

                    index += 1
                
                if words_len > 2:
                    for i in range(0,words_len-1):
                        word_with_syn = words[i].strip()
                        first_2_char = o_stringmanipulation.mid(word_with_syn, 0, 2)
                        if first_2_char.strip().isdigit():
                            word_with_syn = o_stringmanipulation.mid(word_with_syn, 2, len(word_with_syn))                                                
                        lines.append((word_type,word_index,pos,neg,word_with_syn,description),)
                else:                    
                    lines.append((word_type,word_index,pos,neg,word,description),)                    

                print line


        with open(path + file2, 'w') as outfile:
            json.dump(lines, outfile)
        print data
        o_dbinterpreter.insertone_ref_sentiwordnet(lines)

def translate():
    o_dbinterpreter = db_interpreter.dbinterpreter()
    sentilib = o_dbinterpreter.select_sentiword_rows()
  

translate()
#swn = sentiwordnet()
#swn.read_swn_english()





