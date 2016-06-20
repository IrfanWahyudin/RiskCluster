# from parse import *
from pyparsing import Word, alphas
import re
import sqlite3 as sql3
import numpy as np
import scipy as sc


def parser():
	conn = sql3.connect('DB_WORDS')
	c = conn.cursor()
	num_of_part = 8
	bag_of_rows = c.execute('select id,content from mst_corpus where id >=121 order by id')
	i = 0
	doc_id = 121
	# (len(bag_of_rows.fetchall()) + 1) * 8)
	content = [0,0,0,0,'']
	document_contents = []
	bag_of_rows = c.execute('select content from mst_corpus where id >=121  order by id')
	j = 0
	for bor in bag_of_rows:
		try:
			index_of_icrr = [0,""]
			index_of_keuangan = [0,""]
			index_of_struktur = [0,""]
			index_of_bisnis = [0,""]
			index_of_kemampuan = [0,""]
			index_of_legalitas = [0,""]
			index_of_aspeklain = [0,""]
			index_of_kurs = [0,""]
			index_of_trailer = [0,""]
			bag_of_row = str(bor).lower().replace("\\n","")
			
			bag_of_row = bag_of_row.replace("mitigai","mitigasi")
			bag_of_row = bag_of_row.replace("bukopin","xyz")
			
			str(bag_of_row).replace("bukopin","xyz")

			nama_string = 'nama'
			bidang_usaha_string = 'bidang usaha'
			pihak_manajemen_string = 'pihak manajemen'
			poin_string = 'poin risiko'
			mitigasi_string = 'mitigasi risiko'
			trailer_string = 'demikian hal ini'
			nama = str(bag_of_row).find(nama_string)
			bidang = str(bag_of_row).find(bidang_usaha_string)
			pihak_manajemen = str(bag_of_row).find(bidang_usaha_string)
			index_of_icrr[0] = str(bag_of_row).find('pengisian icrr')
			index_of_icrr[1] = 'pengisian icrr'
			index_of_keuangan[0] = str(bag_of_row).find('aspek keuangan')
			index_of_keuangan[1] = 'aspek keuangan'
			index_of_struktur[0] = str(bag_of_row).find('analisis struktur fasilitas')
			index_of_struktur[1] = 'analisis struktur fasilitas'
			index_of_bisnis[0] = str(bag_of_row).find('analisis aspek bisnis')
			index_of_bisnis[1] = 'analisis aspek bisnis'
			index_of_kemampuan[0] = str(bag_of_row).find('analisis kemampuan')
			index_of_kemampuan[1] = 'analisis kemampuan'
			index_of_legalitas[0] = str(bag_of_row).find('analisis terkait legalitas')
			index_of_legalitas[1] = 'analisis terkait legalitas'
			index_of_aspeklain[0] = str(bag_of_row).find('analisis terkait aspek lain')
			index_of_aspeklain[1] = 'analisis terkait aspek lain'
			index_of_kurs[0] = str(bag_of_row).find('analisis terkait kurs')
			index_of_kurs[1] = 'analisis terkait kurs'
			index_of_trailer[0] = str(bag_of_row).find('demikian hal ini')
			index_of_trailer[1] = 'demikian hal ini'
			poin_string = 'poin risiko'
			mitigasi_string = 'mitigasi risiko'
			trailer_string = 'demikian hal ini'

			
			list_of_index = [index_of_icrr, index_of_keuangan, index_of_struktur, index_of_bisnis,
								 index_of_kemampuan, index_of_legalitas, index_of_aspeklain, index_of_kurs, index_of_trailer]
			list_of_index_indices = [index_of_icrr[0], index_of_keuangan[0], index_of_struktur[0], index_of_bisnis[0],
							 index_of_kemampuan[0], index_of_legalitas[0], index_of_aspeklain[0], index_of_kurs[0], index_of_trailer[0]]
			list_of_index_temp1 = [i for i in list_of_index_indices]

			list_of_index_indices.sort()
			list_of_index_sorted = list_of_index_indices

			i = 0
			num_of_index = len(list_of_index_indices)
	
			pr_kemampuan = ""
			pr_keuangan = ""
			pr_pengisian_icrr = ""
			pr_kurs = ""
			pr_fasilitas_kredit = ""
			pr_pengisian_icrr = ""
			pr_aspek_lain = ""
			pr_legalitas = ""
			pr_aspek_bisnis = ""

			mt_kemampuan = ""
			mt_keuangan = ""
			mt_pengisian_icrr = ""
			mt_kurs = ""
			mt_fasilitas_kredit = ""
			mt_pengisian_icrr = ""
			mt_aspek_lain = ""
			mt_legalitas = ""
			mt_aspek_bisnis = ""
			# print num_of_index
			for current_index in list_of_index_indices:
				if i < num_of_index-1 and list_of_index[list_of_index_temp1.index(current_index)][0] > 0:
					next_index = list_of_index_indices[i+1]

					current_part = list_of_index[list_of_index_temp1.index(current_index)][1]
					next_part = list_of_index[list_of_index_temp1.index(next_index)][1]
					# print current_part
					# print next_part
					if current_part == 'pengisian icrr':					
						pengisian_icrr = re.findall(r'' + current_part + '(.*?)' + next_part, bag_of_row, re.DOTALL)[-1]
						try:
							pr_pengisian_icrr = str(re.findall(r'' + current_part + '(.*?)' + mitigasi_string, bag_of_row, re.DOTALL)[-1])			
							# pr_pengisian_icrr = str(re.findall(r'pengisian icrr(.*?)mitigasi risiko', pengisian_icrr, re.DOTALL)[-1])			
							mt_pengisian_icrr = str(re.findall(r'' + mitigasi_string + '(.*?)' + next_part, bag_of_row, re.DOTALL)[-1])
						except:
							print doc_id, pengisian_icrr

						content =[doc_id,1,1,1,pr_pengisian_icrr]					
						document_contents.append(content)
						j+= 1
						content =[doc_id,2,1,1,mt_pengisian_icrr]						
						document_contents.append(content)
						j+= 1
					elif current_part == 'aspek keuangan':
						keuangan = re.findall(r'' + current_part + '(.*?)' + next_part, bag_of_row, re.DOTALL)[-1]	
						pr_keuangan = str(re.findall(r'' + current_part + '(.*?)' + mitigasi_string, bag_of_row, re.DOTALL)[-1])			
						mt_keuangan = str(re.findall(r'' + mitigasi_string + '(.*?)' + next_part, bag_of_row, re.DOTALL)[-1])
						content =[doc_id,1,2,1,pr_keuangan]
						document_contents.append(content)
						j+= 1
						content =[doc_id,2,2,1,mt_keuangan]
						document_contents.append(content)
						j+= 1
					elif current_part == 'analisis aspek bisnis':
						aspek_bisnis = re.findall(r'' + current_part +'(.*?)' + next_part, bag_of_row, re.DOTALL)[-1]
						pr_aspek_bisnis = str(re.findall(r'' + poin_string + '(.*?)' + mitigasi_string, aspek_bisnis, re.DOTALL)[-1])
						mt_aspek_bisnis = str(re.findall(r'' + mitigasi_string + '(.*?)' + next_part, aspek_bisnis + ' ' + next_part, re.DOTALL)[-1])
						content =[doc_id,1,3,1,pr_aspek_bisnis]
						document_contents.append(content)
						j+= 1
						content =[doc_id,2,3,1,mt_aspek_bisnis]
						document_contents.append(content)
						j+= 1
						print mt_aspek_bisnis
					elif current_part == 'analisis kemampuan':
						kemampuan = re.findall(r'' + current_part +'(.*?)' + next_part, bag_of_row, re.DOTALL)[-1]

						try:
							pr_kemampuan = str(re.findall(r'' + poin_string + '(.*?)' + mitigasi_string, kemampuan, re.DOTALL)[-1])
							mt_kemampuan = str(re.findall(r'' + mitigasi_string + '(.*?)' + next_part, kemampuan + next_part, re.DOTALL)[-1])
						except:
							print doc_id, kemampuan							
						content =[doc_id,1,4,2,pr_kemampuan]
						document_contents.append(content)
						j+= 1
						content =[doc_id,2,4,2,mt_kemampuan]
						document_contents.append(content)
						j+= 1
					elif current_part == 'analisis terkait legalitas':
						legalitas = re.findall(r'' + current_part + '(.*?)' + next_part, bag_of_row, re.DOTALL)[-1]
						try:
							pr_legalitas = str(re.findall(r'' + poin_string + '(.*?)' + mitigasi_string, legalitas, re.DOTALL)[-1])
							mt_legalitas = str(re.findall(r'' + mitigasi_string + '(.*?)' + next_part, legalitas + next_part, re.DOTALL)[-1])
						except:
							print doc_id,legalitas
						content =[doc_id,1,5,3,pr_legalitas]
						document_contents.append(content)
						j+= 1
						content =[doc_id,2,5,3,mt_legalitas]
						document_contents.append(content)
						j+= 1
					elif current_part == 'analisis struktur':
						fasilitas_kredit = re.findall(r'' + current_part + '(.*?)' + next_part, bag_of_row, re.DOTALL)[-1]
						pr_fasilitas_kredit = str(re.findall(r'' + poin_string + '(.*?)' + mitigasi_string, fasilitas_kredit, re.DOTALL)[-1])
						mt_fasilitas_kredit = str(re.findall(r'' + mitigasi_string + '(.*?)', fasilitas_kredit, re.DOTALL)[-1])
						content =[doc_id,1,6,3,pr_fasilitas_kredit]
						document_contents.append(content)
						j+= 1
						content =[doc_id,2,6,3,mt_fasilitas_kredit]
						document_contents.append(content)
						j+= 1
					elif current_part == 'analisis terkait aspek lain':
						aspek_lain = re.findall(r'' + current_part + '(.*?)' + next_part, bag_of_row, re.DOTALL)[-1]
						try:
							pr_aspek_lain = str(re.findall(r'' + poin_string + '(.*?)' + mitigasi_string, aspek_lain, re.DOTALL)[-1])
							mt_aspek_lain = str(re.findall(r'' + mitigasi_string + '(.*?)' + next_part, aspek_lain + next_part, re.DOTALL)[-1])
						except:
							print doc_id, aspek_lain
						
						content =[doc_id,1,7,3,pr_aspek_lain]
						document_contents.append(content)
						j+= 1
						content =[doc_id,2,2,3,mt_aspek_lain]
						document_contents.append(content)
						j+= 1
					elif current_part == 'analisis terkait kurs':
						kurs = re.findall(r'' + current_part + '(.*?)' + next_part, bag_of_row, re.DOTALL)[-1]
						pr_kurs = str(re.findall(r'' + poin_string + '(.*?)' + mitigasi_string, kurs, re.DOTALL)[-1])
						mt_kurs = str(re.findall(r'' + mitigasi_string + '(.*?)' + next_part, kurs + next_part, re.DOTALL)[-1])
						content =[doc_id,1,8,3,pr_kurs]
						document_contents.append(content)
						j+= 1
						content =[doc_id,2,8,3,mt_kurs]
						document_contents.append(content)
						j+= 1
					print "Doc #", doc_id
					# print pr_pengisian_icrr
					# sql = 'insert into mst_opini_mitigasi_raw(id, opini_mitigasi, part, cluster_task, content) values(' + str(content[0]) + "," + str(content[1]) + "," + str(content[2]) + "," + str(content[3]) + ",'" + content[4] + "')"
											
					# print sql
					# c.execute(sql)
					# conn.commit()
					# print list_of_index[list_of_index_temp1.index(current_index)][0]
					# print list_of_index[list_of_index_temp1.index(current_index)][1]
					# print list_of_index[list_of_index_temp1.index(next_index)][0]
					# print list_of_index[list_of_index_temp1.index(next_index)][1]
					# print pr_pengisian_icrr
					# print pr_keuangan
					# print pr_aspek_bisnis

					# print pr_kemampuan

					# print pr_fasilitas_kredit
					# print pr_legalitas

					# print pr_kurs				
					# print pr_aspek_lain
					# #--------------------------------------------------------------------
					# print mt_pengisian_icrr
					# print mt_keuangan
					# print mt_aspek_bisnis

					# print mt_kemampuan

					# print mt_fasilitas_kredit
					# print mt_legalitas
					
					# print mt_kurs				
					# print mt_aspek_lain


					
				else:
					print 'part is not defined in document'
				i+=1	
				
				# print j
				

		except RuntimeError, IndexError:
			print "error"
		doc_id+=1

	conn.text_factory = str
	c = conn.cursor()
	# c.execute('delete from mst_opini_mitigasi_raw')
	# conn.commit()
	c.executemany('insert into mst_opini_mitigasi_raw values(?,?,?,?,?)',document_contents)
	conn.commit()
	conn.close()
	# #

	# for bor in bag_of_row:
	# 	if bor.strip() !=  "":
	# 		print parse("mitigasi risiko : {}", bor)

parser()