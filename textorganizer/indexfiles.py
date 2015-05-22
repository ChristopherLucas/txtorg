#!/usr/bin/env python

from whoosh.fields import *
from whoosh.index import create_in

from whoosh.analysis import SimpleAnalyzer

import sys, os, threading, time

from datetime import datetime
import uuid
from preprocessing import *

"""
This class is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer, args_dir = None):
        self.args_dir = args_dir
        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        schema = Schema(name=TEXT(stored=True),
                    path=ID(stored=True),
                    txtorg_id=ID(stored=True),
                    contents=TEXT(stored=False,vector=True,analyzer=analyzer()))
        ix = create_in(storeDir, schema)
        writer = ix.writer()
        print analyzer
        
        print 'document dir is', root
        self.indexDocs(root, writer)

        print 'optimizing index',
        writer.commit(optimize=True)
        print 'done'

    def indexDocs(self, root, writer):
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith(('.txt','.xml')):
                    continue
                print "adding", filename
                try:
                    path = os.path.join(root, filename)
                    file = open(path)
                    contents = unicode(file.read(), 'UTF-8')
                    contents = preprocess(contents, self.args_dir)
                    file.close()
                    print contents
                    print type(contents)
                    writer.add_document(name=unicode(filename,'UTF-8'),
                                        path=unicode(os.path.realpath(path),'UTF-8'),
                                        txtorg_id=unicode(str(uuid.uuid1()),'UTF-8'),
                                        contents=contents)
                    
                    if len(contents) == 0:
                        print "warning: no content in %s" % filename
                except Exception, e:
                    print "Failed in indexDocs:", e
