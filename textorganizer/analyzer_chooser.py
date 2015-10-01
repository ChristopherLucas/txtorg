from Tkinter import *
import time, thread, threading
from whoosh.analysis import StandardAnalyzer, SimpleAnalyzer, StopFilter
import whoosh
from chinese import ChineseAnalyzer
from arabic import ArabicAnalyzer
from collections import defaultdict

# Next time?  http://textminingonline.com/dive-into-nltk-part-vi-add-stanford-word-segmenter-interface-for-python-nltk

try:
    import lucene
    haslucene = True
    from fromlucene import LuceneTokenizer
    from org.apache.lucene.analysis.ar import ArabicAnalyzer as AA_lucene
    from org.apache.lucene.analysis.hy import ArmenianAnalyzer
    from org.apache.lucene.analysis.eu import BasqueAnalyzer
    from org.apache.lucene.analysis.br import BrazilianAnalyzer
    from org.apache.lucene.analysis.bg import BulgarianAnalyzer
    from org.apache.lucene.analysis.ca import CatalanAnalyzer
    from org.apache.lucene.analysis.cjk import CJKAnalyzer
    from org.apache.lucene.analysis.standard import ClassicAnalyzer
    from org.apache.lucene.analysis.cz import CzechAnalyzer
    from org.apache.lucene.analysis.da import DanishAnalyzer
    from org.apache.lucene.analysis.en import EnglishAnalyzer
    from org.apache.lucene.analysis.fi import FinnishAnalyzer
    from org.apache.lucene.analysis.fr import FrenchAnalyzer
    from org.apache.lucene.analysis.gl import GalicianAnalyzer
    from org.apache.lucene.analysis.de import GermanAnalyzer
    from org.apache.lucene.analysis.el import GreekAnalyzer
    from org.apache.lucene.analysis.hi import HindiAnalyzer
    from org.apache.lucene.analysis.hu import HungarianAnalyzer
    from org.apache.lucene.analysis.id import IndonesianAnalyzer
    from org.apache.lucene.analysis.ga import IrishAnalyzer
    from org.apache.lucene.analysis.it import ItalianAnalyzer
    from org.apache.lucene.analysis.lv import LatvianAnalyzer
    from org.apache.lucene.analysis.no import NorwegianAnalyzer
    from org.apache.lucene.analysis.fa import PersianAnalyzer
    from org.apache.lucene.analysis.pt import PortugueseAnalyzer
    from org.apache.lucene.analysis.ro import RomanianAnalyzer
    from org.apache.lucene.analysis.ru import RussianAnalyzer
    from org.apache.lucene.analysis.ckb import SoraniAnalyzer
    from org.apache.lucene.analysis.es import SpanishAnalyzer
    from org.apache.lucene.analysis.standard import StandardAnalyzer as SA_Lucene
    from org.apache.lucene.analysis.core import StopAnalyzer
    from org.apache.lucene.analysis.sv import SwedishAnalyzer
    from org.apache.lucene.analysis.th import ThaiAnalyzer
    from org.apache.lucene.analysis.tr import TurkishAnalyzer
    from org.apache.lucene.analysis.standard import UAX29URLEmailAnalyzer

    lucenelist = ['Arabic Analyzer', 'Armenian Analyzer', 'Basque Analyzer', 'Brazilian Analyzer', 'Bulgarian Analyzer', 'Catalan Analyzer', 'CJK Analyzer', 'Classic Analyzer', 'Czech Analyzer', 'Danish Analyzer', 'English Analyzer', 'Finnish Analyzer', 'French Analyzer', 'Galician Analyzer', 'German Analyzer', 'Greek Analyzer', 'Hindi Analyzer', 'Hungarian Analyzer', 'Indonesian Analyzer', 'Irish Analyzer', 'Italian Analyzer', 'Latvian Analyzer', 'Norwegian Analyzer', 'Persian Analyzer', 'Portuguese Analyzer', 'Romanian Analyzer', 'Russian Analyzer', 'Sorani Analyzer', 'Spanish Analyzer', 'Standard Analyzer', 'Stop Analyzer', 'Swedish Analyzer', 'Thai Analyzer', 'Turkish Analyzer', 'UAX29URLEmail Analyzer']
    lucenefs = [AA_lucene,ArmenianAnalyzer,BasqueAnalyzer,BrazilianAnalyzer,BulgarianAnalyzer,CatalanAnalyzer,CJKAnalyzer,ClassicAnalyzer,CzechAnalyzer,DanishAnalyzer,EnglishAnalyzer,FinnishAnalyzer,FrenchAnalyzer,GalicianAnalyzer,GermanAnalyzer,GreekAnalyzer,HindiAnalyzer,HungarianAnalyzer,IndonesianAnalyzer,IrishAnalyzer,ItalianAnalyzer,LatvianAnalyzer,NorwegianAnalyzer,PersianAnalyzer,PortugueseAnalyzer,RomanianAnalyzer,RussianAnalyzer,SoraniAnalyzer,SpanishAnalyzer,SA_Lucene,StopAnalyzer,SwedishAnalyzer,ThaiAnalyzer,TurkishAnalyzer,UAX29URLEmailAnalyzer]
except:
    haslucene = False


class AnalyzerChooser:
    #def __init__(self):    
    def __init__(self, parent):
        self.main_gui = parent
        #self.root = Toplevel()
        self.root = Toplevel(parent.root)        
        r = self.root

        print 'parent', parent
        print 'root', r
        
        r.title('Choose your Analyzer')

        self.analyzers = [StandardAnalyzer, SimpleAnalyzer, ChineseAnalyzer, ArabicAnalyzer]
        self.analyzerliststr = ['English StandardAnalyzer', "English SimpleAnalyzer", "SnowNLP Chinese", "Nielsen Arabic Analyzer"]
        # hardcoded, :(
        langs = whoosh.lang.languages
        #langs = ('ar', 'da', 'nl', 'fi', 'fr', 'de', 'hu', 'it', 'no', 'pt', 'ro', 'ru', 'es', 'sv', 'tr')
        aliases = ('Arabic','Danish','Dutch','English','Finnish','French','German','Hungarian','Italian','Norwegian','Portuguese','Romanian','Russian','Spanish','Swedish','Turkish')

        for (l,a) in zip(langs,aliases):
            self.analyzerliststr.append(a + ' Analyzer (Whoosh)')
            self.analyzers.append(whoosh.analysis.LanguageAnalyzer(l))

        if haslucene:
            for (name,fn) in zip(lucenelist,lucenefs):
                print name, fn
                self.analyzerliststr.append(name + ' (Lucene)')
                self.analyzers.append(LuceneTokenizer(fn))

        print self.analyzers
                
        f = PanedWindow(r, showhandle=True)
        lf = PanedWindow(f, relief=GROOVE, borderwidth=2,showhandle=True)
        f.pack(fill=BOTH,expand=1)
        Label(lf, text="Analyzer").pack(pady=10,padx=10)

        # Items in the left frame
        self.analyzerlist = Listbox(lf, exportselection=False)
        corpusscroll = Scrollbar(lf, command=self.analyzerlist.yview)
        self.analyzerlist.configure(yscrollcommand=corpusscroll.set)
        self.analyzerlist.pack(side=LEFT,fill=BOTH, expand=1)
        corpusscroll.pack(side=LEFT, fill=Y)
        lf.pack(side=LEFT,fill=BOTH, expand=1,pady=10,padx=10)

        # Items in the right frame
        cf = PanedWindow(f, relief=GROOVE, borderwidth=2,showhandle=True)
        Label(cf, text="Sample").pack(pady=10,padx=10)

        cft = PanedWindow(cf, borderwidth=2,showhandle=True)
        cfb = PanedWindow(cf, borderwidth=2,showhandle=True)

        self.e = Entry(cft,state=DISABLED)
        self.e.pack(side=LEFT,fill=BOTH,expand=1)

        self.e.delete(0, END)
        self.e.configure(state=NORMAL)
        self.e.insert(0, "Type text here to test each analyzer.")

        self.analyzebutton = Button(cft, text="Tokenize",state=DISABLED,command=self.updateTokens)
        self.analyzebutton.pack(side=LEFT, padx=5, pady=8)

        self.tokentext = Text(cfb)

        self.tokentext.insert(END,"Tokens:")

        self.tokentext.pack()

        cft.pack(expand=1,fill=BOTH)
        cfb.pack(fill=X)
        cf.pack(side=LEFT,expand=1,fill=BOTH,pady=10,padx=10)



        # Pack it all into the main frame

        buttonframe = Frame(r)
        Button(buttonframe, text="Cancel", command=self.cancel).pack(side=LEFT,padx=5,pady=8)
        Button(buttonframe, text="OK", command=self.ok).pack(side=LEFT)
        buttonframe.pack(side=TOP)
        f.pack()
        # set up event handling

        # populate fields and run the gui

        self.updateAnalyzer()

        # poll for changes in the list
        self.current = None
        self.poll()
        #self.root.mainloop()
        print "Done?? 999"

    def ok(self):
        analyzeridx = self.analyzerlist.curselection() # was curselection
        if len(analyzeridx)==0:
            self.cancel()
            return
        analyzeridx = int(analyzeridx[0])
        analyzerstr = self.analyzerliststr[analyzeridx]
        if 'Lucene' in analyzerstr or 'Whoosh' in analyzerstr:
            analyzer = lambda: self.analyzers[analyzeridx]
        else:
            analyzer = self.analyzers[analyzeridx]
        self.main_gui.write({'set_analyzer': (analyzerstr, analyzer)})
        print "self.root:", self.root
        self.root.destroy()
        print 'Destroyed analyzer chooser'

    def cancel(self):
        self.root.destroy()

    # def after(self, wait, func):   # passed time in msecs, function to call.
    #     # run the function in a new thread, so it won't hang main script
    #     print "Aftering."
    #     thread.start_new_thread(self.delay, (wait, func))

    def delay(self, wait, func):
        time.sleep(wait * .001)    # convert msecs into secs and delay this thread
        func()	                          # call the function passed as a parameter

    def updateAnalyzer(self):
        """update the list of items in the corpus"""
        for item in self.analyzerliststr:
            self.analyzerlist.insert(END, item)

    def updateTokens(self):
        """update the numbers displayed for the documents and terms"""

        # Perform the search and return the number of terms and documents
        print "Update tokens"
        # Update the GUI
        self.tokentext.configure(state=NORMAL)

        self.tokentext.delete(1.0,END)
        self.tokentext.insert(END,"Tokens: ")

        analyzeridx = self.analyzerlist.curselection() # was curselection        
        if len(analyzeridx)==0:
            return
        analyzeridx = int(analyzeridx[0])
        analyzerstr = self.analyzerliststr[analyzeridx]
        if 'Lucene' in analyzerstr or 'Whoosh' in analyzerstr:
            analyzer = lambda: self.analyzers[analyzeridx]
        else:
            analyzer = self.analyzers[analyzeridx]
        
        #print analyzer
        #print int(analyzerstr[0])
        #print analyzer

        print "Selected analyzer"

        # some thread nonsense?
        #self.curlucene.attachCurrentThread()
        #tokenStream = analyzer.tokenStream("contents", lucene.StringReader(self.e.get()))
        #term = tokenStream.addAttribute(lucene.TermAttribute.class_)
        #termA = lucene.TermAttributeImpl()

        if len(self.e.get())>0:
            print 'Analyzer:', analyzer
            print 'self.e.get, whatever that is:', self.e.get()            
            athread = AnalyzerThread(analyzer,unicode(self.e.get()))
            athread.start()
            athread.join()
            print athread.tokens
            tokens = [t.text for t in athread.tokens]
            print tokens
            for term in tokens:
                self.tokentext.insert(END, "[%s]" %(term))


    def resetTokens(self):
        """reset the numbers displayed for the documents and terms"""
        self.tokentext.configure(state=NORMAL)
        self.tokentext.delete(1.0,END)
        self.tokentext.insert(END,"Tokens: ")
        self.tokentext.configure(state=DISABLED)

    def poll(self):
        try:
            now = self.analyzerlist.curselection()
        except TclError:
            return
        if now != self.current:
            self.current = now
        # is anything selected?
        if len(now)>0:
            self.analyzebutton.configure(state=NORMAL)
        self.root.after(25, self.poll)
        #self.after(10, self.poll)

        
class AnalyzerThread(threading.Thread):
    def __init__(self,analyzer,string):
         super(AnalyzerThread, self).__init__()
         self.analyzer=analyzer()
         self.string = string
         self.tokens = []
    def run(self):
        self.tokens = self.analyzer(self.string)

if __name__ == "__main__":
    ac = AnalyzerChooser()
