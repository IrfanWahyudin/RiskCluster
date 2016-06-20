import numpy as np
#import sklearn as sk
import scipy as sc
import sqlite3 as sql3
import goslate

class dbinterpreter():
    def insertbulk_rawdoc_content(self,contents):
        conn = sql3.connect('DB_WORDS')
        conn.text_factory = str
        c = conn.cursor()
        # c.execute('delete from mst_corpus')
        # conn.commit()
        c.executemany('insert into mst_corpus values(?,?)', contents)
        conn.commit()
        conn.close()

    def selectone_rawdoc_content(self):
        dtraw = np.dtype([('id',np.int,1),
                          ('dirtywords',basestring,1),
                          ('cleanwords',basestring,1)])
        #dtbow = np.dtype([('',np.),
        #                  ()])
        rawdocs = np.array([(1,'the sky is blue',''),
                            (2,'the sun is bright',''),
                            (3,'i stand under the bright blue sky','')],
                            dtype = dtraw)
        wordlist = np.array([('word',np.str_,30),
                             ('idf',np.int32,)])

        conn = sql3.connect('DB_WORDS')

        c = conn.cursor()

        c.execute('select * from mst_corpus')
        print c.fetchone()

    def insertone_ref_sentiwordnet(self, lines):
        conn = sql3.connect('DB_WORDS')
        conn.text_factory = str
        c = conn.cursor()
        c.executemany('insert into ref_sentiwordnet values(?,?,?,?,?,?)', lines)
        conn.commit()
        conn.close()

    def select_sentiword_rows(self):
        conn = sql3.connect('DB_WORDS')
        sentilib = conn.execute('SELECT * FROM ref_sentiwordnet_nodesc WHERE  word_id is null')
        #sentilib = conn.execute('SELECT * FROM ref_sentiwordnet_nodesc WHERE  CAST(word_index as decimal) > 187049')
        gs = goslate.Goslate()
        countsentilib = sentilib.rowcount

        sentiword_en = ''
        sentiword_id = ''
        sqls = ['' for x in range(0,207000)]
        update_key = ['','']
        k = 0
        try:
            for r in sentilib:
                sentiword_en = str(r[4]).replace('','').replace("'","''")
                sentiword_id = str(gs.translate(str(r[4]).replace('_',' '),'id')).replace("'","''")
                
                
                update_key[0] = r[1]
                update_key[1] = sentiword_en
                sql = "UPDATE ref_sentiwordnet_nodesc SET word_id = '" + sentiword_id +  "'  WHERE word_index = '" + update_key[0]  + "'  AND word_en = '" + update_key[1] + "'"
                conn.execute(sql)
                conn.commit()
                sqls[k] = sql            
                print k, ' - ', update_key[0],  ' - ' , sentiword_en, ' - ', sentiword_id
                k+=1
        except (RuntimeError, TypeError, NameError):
               print 'oops'

        for m in range(0,k):
            print m, ' - ' , sqls[m]
           
        conn.close()
        return sentilib
            


#for item in rawdocs:
#    print item['dirtywords'].split(' ')

        
#print bow[0]['id']


#class 



