import i_db_interpreter as db_interpreter
import i_docx_reader as docx_reader
import datetime 
class main(object):
    """description of class"""
    
    def run_main(self):
        o_docxreader = docx_reader.docxreader()
        o_dbinterpreter = db_interpreter.dbinterpreter()

        rawdoc = o_docxreader.read_all_files()
        sizeofrawdoc = len(rawdoc)

        if sizeofrawdoc > 0:
            o_dbinterpreter.insertbulk_rawdoc_content(rawdoc)
            print "dokumen sukses diekspor..."
        else:
            print "tidak ada file yang dibaca..."

m = main()
m.run_main()