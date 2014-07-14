#!/usr/bin/env python

import sys, os, lucene, threading, time
try:
    from lucene import Field, SimpleFSDirectory, File, IndexWriter, Document
except:
    from org.apache.lucene.document import Field
    from java.io import File
    from org.apache.lucene.store import SimpleFSDirectory
    from org.apache.lucene.index import IndexWriter
    from org.apache.lucene.document import Document

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

        store = SimpleFSDirectory(File(storeDir))
        writer = IndexWriter(store, analyzer, False,
                                    IndexWriter.MaxFieldLength.LIMITED)
        writer.setMaxFieldLength(1048576)
        print 'document dir is', root
        self.indexDocs(root, writer)

        print 'optimizing index',
        writer.optimize()
        writer.close()
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
                    doc = Document()
                    doc.add(Field("name", filename,
                                         Field.Store.YES,
                                         Field.Index.NOT_ANALYZED))
                    doc.add(Field("path", os.path.realpath(path),
                                         Field.Store.YES,
                                         Field.Index.NOT_ANALYZED))
                    doc.add(Field("txtorg_id", str(uuid.uuid1()),
                                         Field.Store.YES,
                                         Field.Index.NOT_ANALYZED))
                    if len(contents) > 0:
                        doc.add(Field("contents", contents,
                                             Field.Store.NO,
                                             Field.Index.ANALYZED,
                                             Field.TermVector.YES))
                    else:
                        print "warning: no content in %s" % filename
                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e
