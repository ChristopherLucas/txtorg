#from whoosh.reading import iter_docs

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

    for doc in reader.iter_docs():
        print "get fields?"

    for field_name in reader.indexed_field_names():
        all_fields[field_name] = reader.field_terms(field_name)

    return(dict(all_fields))

    # for i in xrange(reader.maxDoc()):
    #     if reader.isDeleted(i): continue
    #     doc = reader.document(i)
    #     for f in doc.getFields():
    #         field = Field.cast_(f)
    #         if len(all_fields[field.name()]) < max_vals: all_fields[field.name()].add(field.stringValue())

    # return dict(all_fields)
