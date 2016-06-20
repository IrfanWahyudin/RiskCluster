import os
import suku
from hmmtagger import MainTagger
from tokenization import *
from html2text import *
from termextract import *
from summary import *
from capschunking import *


mt = None
def postag():
    return { 'apptitle':'pebahasa', 'root':request.environ.get('SCRIPT_NAME') }

def init_tag():
    global mt
    print 'mt',mt
    if mt is None:
        print 'MainTagger'
        mt = MainTagger("resource/Lexicon.trn", "resource/Ngram.trn", 0, 3, 3, 0, 0, False, 0.2, 0, 500.0, 1)
        
def do_tag(kalimat):
    lines = kalimat.strip().split("\n")
    result = []
    try:
        # print lines
        init_tag()
        for l in lines:
            if len(l) == 0: continue
            out = sentence_extraction(cleaning(l))
            for o in out:
                strtag = " ".join(tokenisasi_kalimat(o)).strip()
                result += [" ".join(mt.taggingStr(strtag))]
    except:
        return "Error Exception"
    return "\n".join(result)

# print do_tag("terdapat agunan fix asset (tanah dan bangunan) dan tagihan sehingga perlu dipastikan mengenai legalitas pengikatan, mekanisme penanganan dan monitoring atas kualitas dan nilai terkini dari agunan tersebut.eksekusi atas jaminan yang berupa non fixed asset (peralatan) bukan merupakan hal yang mudah dan sangat rentan terhadap penurunan nilai/depresiasi (terlihat dari aset tetap dari tahun 2010-2102 yang nilainya terus menurun)")