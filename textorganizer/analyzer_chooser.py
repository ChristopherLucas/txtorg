from Tkinter import *
import tkFileDialog
import re
import math,random
import os, sys, lucene, thread, time
from lucene import Version

analyzerlist = ["StopAnalyzer", "SimpleAnalyzer", "WhitespaceAnalyzer", "StandardAnalyzer", "ArabicAnalyzer", "ArmenianAnalyzer", "BasqueAnalyzer", \
     "BulgarianAnalyzer", "BrazilianAnalyzer", "CatalanAnalyzer", "CJKAnalyzer", "CzechAnalyzer", "DanishAnalyzer", "DutchAnalyzer", \
     "FinnishAnalyzer", "FrenchAnalyzer", "GalicianAnalyzer", "GermanAnalyzer", "GreekAnalyzer", "HindiAnalyzer", "HungarianAnalyzer", \
     "IndonesianAnalyzer", "ItalianAnalyzer", "LatvianAnalyzer", "NorwegianAnalyzer", "PersianAnalyzer", "PortugueseAnalyzer", \
     "RomanianAnalyzer", "RussianAnalyzer", "SwedishAnalyzer", "ThaiAnalyzer", "TurkishAnalyzer"]

from . import stemmingtools

class AnalyzerChooser:
    def __init__(self, parent):
        self.main_gui = parent
        self.curlucene = lucene.initVM()        
        r = self.root = Toplevel()
        self.root.title('txtorg')   

        self.analyzers = []
        self.analyzerliststr = []

        for a in analyzerlist:
            try:
                exec('from lucene import '+a)
                exec('self.analyzers.append('+a+'(Version.LUCENE_CURRENT))')
                exec('self.analyzerliststr.append("'+a+'")')
            except:
                print "Analyzer not present", a
                        
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

        self.searchbutton = Button(cft, text="Tokenize",state=DISABLED,command=self.updateTokens)
        self.searchbutton.pack(side=LEFT, padx=5, pady=8)

        self.tokentext = Text(cfb)

        self.tokentext.insert(END,"Documents: 0")

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

        #self.analyzerlist.bind('<ButtonRelease-1>',lambda x: self.updateMetadata()
        #self.analyzerlist.bind('<Key>',lambda x: self.updateMetadata())        

        # populate fields and run the gui
        
        self.updateAnalyzer()

        # poll for changes in the list
        self.current = None
        self.poll()
        self.root.mainloop()

    def ok(self):
        analyzeridx = self.analyzerlist.curselection() # was curselection
        if len(analyzeridx)==0:
            self.cancel()
            return
        analyzeridx = int(analyzeridx[0])
        analyzer = self.analyzers[analyzeridx]
        analyzerstr = self.analyzerliststr[analyzeridx]
        self.main_gui.write({'set_analyzer': (analyzerstr, analyzer)})
        self.root.destroy()

    def cancel(self):
        self.root.destroy()

    def after(self, wait, func):   # passed time in msecs, function to call.
        # run the function in a new thread, so it won't hang main script
        thread.start_new_thread(self.delay, (wait, func))

    def delay(self, wait, func):
        time.sleep(wait * .001)    # convert msecs into secs and delay this thread
        func()	                          # call the function passed as a parameter
        
    def updateAnalyzer(self):
        """update the list of items in the corpus"""
        for item in self.analyzerliststr:
            self.analyzerlist.insert(END, item)

    def getCorpus(self):        
        """return the list of selected items in the corpus"""
        items = self.analyzerlist.curselection()        
        itemstr = [self.analyzerlist.get(int(item)) for item in items]

        return itemstr
            
    def updateMetadata(self):
        """update the metadata field to reflect the tags from the selected corpus"""                        
        # enable clicking on these
        self.searchbutton.configure(state=NORMAL)
        self.e.configure(state=NORMAL)

        self.resetTokens()
        self.updateTokens()
        
    def updateTokens(self):
        """update the numbers displayed for the documents and terms"""               

        # Perform the search and return the number of terms and documents        
        print "Update tokens"
        # Update the GUI
        self.tokentext.configure(state=NORMAL)
        
        self.tokentext.delete(1.0,END)
        self.tokentext.insert(END,"Tokens: ")

        analyzerstr = self.analyzerlist.curselection() # was curselection
        if len(analyzerstr)==0:
            return
        analyzer = self.analyzers[int(analyzerstr[0])]

        print "Selected analyzer"

        self.curlucene.attachCurrentThread()
        
        tokenStream = analyzer.tokenStream("contents", lucene.StringReader(self.e.get()))
        term = tokenStream.addAttribute(lucene.TermAttribute.class_)

        termA = lucene.TermAttributeImpl()

        if len(self.e.get())>0:
            while tokenStream.incrementToken():
                # Note: in Lucene 2.9.4, for some reason this Attribute is not a TermAttribute
                # This is a bug.  The hacky way around it is to parse the toString() result manually.
                if lucene.VERSION=='2.9.4':
                    mys = term.toString()
                    tokenstring = re.findall('\((.*?),',mys)[0]
                    self.tokentext.insert(END, "[%s]" %(tokenstring))
                else:
                    self.tokentext.insert(END, "[%s]" %(term.term()))
                

    def resetTokens(self):
        """reset the numbers displayed for the documents and terms"""                
        self.tokentext.configure(state=NORMAL)

        numDocs = 0
        numTerms = 0
        
        self.tokentext.delete(1.0,END)
        self.tokentext.insert(END,"Tokens: ")
                
        self.tokentext.configure(state=DISABLED)

    def poll(self):
        try:
            now = self.analyzerlist.curselection()
        except TclError:
            return
        if now != self.current:
            self.updateMetadata()            
            self.current = now
        self.after(250, self.poll)
