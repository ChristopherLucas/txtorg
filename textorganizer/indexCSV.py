#!/usr/bin/env python

from whoosh.fields import *
from whoosh.index import create_in

import sys, os, threading, time, codecs

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

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

        
class IndexCSV(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, storeDir, analyzer, csvlocation, content_field = None, args_dir = None):
        print "Running IndexCSV"
        self.args_dir = args_dir
        if not os.path.exists(storeDir):
            os.mkdir(storeDir)
            

        if content_field is None:
            schema = Schema(
                txtorg_id=ID(stored=True),
                contents=TEXT(stored=False,vector=True,analyzer=analyzer()))
        else:
            schema = Schema(
                txtorg_id=ID(stored=True))
        ix = create_in(storeDir, schema)
        writer = ix.writer()
        # pull the metadata from the csv header to make the schema
        print "csv location:", csvlocation
        
        ucr = unicode_csv_reader(codecs.open(csvlocation, encoding='UTF-8'), delimiter=',', quotechar='"')
        header = ucr.next()
        for (i,h) in enumerate(header):
            # exclude the path in the schema
            h = h.strip()
            print h
            if content_field is not None and content_field==h:
                writer.add_field(h, TEXT(stored=False,vector=True,analyzer=analyzer()))
                ind = i
            else:
                writer.add_field(h, ID(stored=True))

        self.changed_rows = 0
        try:
            for row in ucr:
                print row # row is a list.
                if content_field is not None:
                    print "Import csv with content."
                    # where is the content_field in the row?
                    contents = row[ind]
                else:
                    path = row[0]
                    f = open(path)
                    # should probably use chardet here...
                    contents = unicode(f.read(), 'UTF-8')
                    contents = preprocess(contents, self.args_dir)
                    f.close()
                print contents

                # i'm so sorry. :(
                # writer.add_document(txtorg_id=unicode(str(uuid.uuid1()),'UTF-8'),filepath=u'./examples/brothersk/1.txt', book=u'2', chapter=u'2',contents=contents)
                args = []
                print row
                for (i,k) in enumerate(row):
                    args.append(u'{}=u"{}"'.format(header[i],k))
                if content_field is None:
                    docaddstring = u"writer.add_document(txtorg_id=unicode(str(uuid.uuid1()),'UTF-8'),{},contents=contents)".format(u','.join(args))
                else:
                    docaddstring = u"writer.add_document(txtorg_id=unicode(str(uuid.uuid1()),'UTF-8'),{})".format(u','.join(args))
                print docaddstring
                eval(docaddstring)
                if len(contents) == 0:
                    print "warning: no content in %s" % filename
                self.changed_rows += 1
        except Exception, e:
            print "Failed in indexCSV:", e

        
        print 'optimizing index',
        writer.commit(optimize=True)
        print 'done'
        self.index = ix
        self.writer = writer
        self.reader = ix.reader()
