try:
    from lucene import \
    SimpleFSDirectory, File, IndexReader, Term, Term, IndexWriter, Version, StandardAnalyzer, TermQuery, IndexSearcher, Document, Field
except:
    from org.apache.lucene.store import SimpleFSDirectory
    from java.io import File
    from org.apache.lucene.index import IndexReader
    from org.apache.lucene.index import Term
    from org.apache.lucene.index import IndexWriter
    from org.apache.lucene.util import Version
    from org.apache.lucene.analysis.standard import StandardAnalyzer
    from org.apache.lucene.search import TermQuery
    from org.apache.lucene.search import IndexSearcher
    from org.apache.lucene.document import Field
    from org.apache.lucene.document import Document
    

import threading, sys, time, os, csv, re, codecs, shutil
from collections import defaultdict

def reindex_all(reader, writer, analyzer):
    for i in xrange(reader.maxDoc()):
        if reader.isDeleted(i): continue
        doc = reader.document(i)
        p = doc.get("path")
        pkid = doc.get('txtorg_id')
        if p is None:
            # No filepath specified, just use original document
            writer.updateDocument(Term("txtorg_id",pkid),doc,analyzer)
        else:
            # if a path field is found, try to read the file it points to and add a contents field
            edited_doc = Document()
            for f in doc.getFields():
                edited_doc.add(Field.cast_(f))

            try:
                inf = open(p)
                contents = unicode(inf.read(), 'UTF-8')
                inf.close()

                if len(contents) > 0:
                    edited_doc.add(Field("contents", contents,
                                         Field.Store.NO,
                                         Field.Index.ANALYZED,
                                         Field.TermVector.YES))
                else:
                    print "warning: no content in %s" % filename
            except:
                print "Could not read file; skipping"
            writer.updateDocument(Term("txtorg_id",pkid),edited_doc,analyzer)


def delete_index(index_path):
    shutil.rmtree(index_path)

def get_fields_and_values(reader, max_vals = 30):
    all_fields = defaultdict(set)

    for i in xrange(reader.maxDoc()):
        if reader.isDeleted(i): continue
        doc = reader.document(i)
        for f in doc.getFields():
            field = Field.cast_(f)
            if len(all_fields[field.name()]) < max_vals: all_fields[field.name()].add(field.stringValue())

    return dict(all_fields)

# class IndexManager():
#     def __init__(self, reader=None, searcher=None, writer=None):
#         self.reader = reader
#         self.searcher = searcher
#         self.writer = writer

#     def get_broken_index_items(self):
#         l = []
#         for i in xrange(self.reader.maxDoc()):
#             if self.reader.isDeleted(i): continue
#             doc = self.reader.document(i)
#             if not os.path.isfile(doc.get("path")):
#                 l.append(doc)
#         return l

#     def cleanup_index(self):
#         broken_docs = self.get_broken_index_items()
#         print "%s broken links found. Enter 'v' to view, 'd' to delete all index items with broken links, or 'q' to cancel" % (len(broken_docs),)
#         while True:
#             choice = raw_input('> ')
#             if choice not in ['v', 'd', 'q']:
#                 print "Invalid input. Enter 'v' to view, 'd' to delete all index items with broken links, or 'q' to cancel"
#                 continue
#             elif choice == 'v':
#                 for d in broken_docs:
#                     print d.get("path")
#                 print "Enter 'd' to delete all index items with broken links, or 'q' to cancel"
#                 continue
#             elif choice =='q':
#                 return
#             elif choice == 'd':
#                 break

#         for d in broken_docs:
#             fp = d.get("path")
#             print "Deleting", fp
#             self.writer.deleteDocuments(Term("path",fp))

#         self.writer.close()


#     def reindex(self, scoreDocs, analyzer):

#         for scoreDoc in scoreDocs:
#             doc = self.searcher.doc(scoreDoc.doc)
#             filepath = doc.get('path')
#             new_doc = self.reassemble_doc(doc,filepath)
#             self.writer.updateDocument(Term("path",filepath),new_doc,analyzer)

#         print "Optimizing index..."
#         self.writer.optimize()
#         self.writer.close()




#     def reassemble_doc(self, lucenedoc):

#         edited_doc = Document()
#         for f in lucenedoc.getFields():
#             edited_doc.add(Field.cast_(f))


#         # Now, add back the unstored "contents" field
#         try:
#             file = open(filepath)
#             contents = unicode(file.read(), 'UTF-8')
#             file.close()

#             if len(contents) > 0:
#                 edited_doc.add(Field("contents", contents,
#                                      Field.Store.NO,
#                                      Field.Index.ANALYZED,
#                                      Field.TermVector.YES))
#             else:
#                 print "warning: no content in %s" % filename
#         except:
#             print "Could not read file; skipping"
#             return None

#         return edited_doc
