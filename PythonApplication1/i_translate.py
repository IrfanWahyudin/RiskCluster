import numpy as np
#import sklearn as sk
import scipy as sc
import sqlite3 as sql3
import goslate

def translate():
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

translate()