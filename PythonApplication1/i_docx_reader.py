import sys
for pth in sys.path:
    print pth
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import sys
import zipfile
import os
import numpy as np

       
class docxreader():
    
      
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'
    PROJECT_PATH = 'C:\\Users\\irfan\\Documents\\Library\\Thesis\\OpiniKredit\\Cleansed\\'

    DT = np.dtype([('id',np.int,4),
                       ('words',basestring,1)])
    def get_docx_text(self, path):
        """
        Take the path of a docx file as argument, return the text in unicode.
        """
        document = zipfile.ZipFile(path)
        xml_content = document.read('word/document.xml')
        document.close()
        tree = XML(xml_content)
 
        paragraphs = []
        for paragraph in tree.getiterator(self.PARA):
            texts = [node.text
                     for node in paragraph.getiterator(self.TEXT)
                     if node.text] 

            if texts:
                paragraphs.append(''.join(texts))
 
        return '\n\n'.join(paragraphs)


    def read_all_files(self):
        #for filename in os.listdir(os.getcwd()): #Gunakan untuk scan semua folder di drive
        i = 121
        rawdoc = []
        
        for filename in os.listdir(self.PROJECT_PATH):
            raw_text =  self.get_docx_text(self.PROJECT_PATH + filename)
            readable_text = raw_text.encode('utf-8').strip()
            rawdoc.append([i,readable_text])
            i=i+1
            
        return rawdoc




