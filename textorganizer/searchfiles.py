#!/usr/bin/env python

#    from lucene import \
#    QueryParser, IndexSearcher, SimpleFSDirectory, File, \
#    VERSION, initVM, Version, IndexReader, TermQuery, Term, Field, MatchAllDocsQuery
from whoosh.qparser import QueryParser

import threading, sys, time, os, csv, re, codecs
from shutil import copy2
import cStringIO
"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.
"""

# from http://stackoverflow.com/questions/5838605/python-dictwriter-writing-utf-8-encoded-csv-files
class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
#        self.writer.writerow({k:v.encode("utf-8") for k,v in D.items()})

        row = {}
        for k, v in D.items():
            if type(v)=='str':
                row[k] = v.encode("utf-8")
            else:
                row[k] = v

        self.writer.writerow(row)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        # data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


def run(index, searcher, analyzer, reader, command, content_field="contents"):


    print 'content_field is', content_field
    """check to see whether the user specified a field"""
    print command
    if command == 'all':
        myresults = reader.all_doc_ids()
        print 'Query Completed'
    else:
        query = QueryParser(content_field,schema=index.schema).parse(command)
        myresults = searcher.docs_for_query(query)
        print 'Query Completed'

    allDicts = []
    allTerms = set()
    allMetadata = []
    termsDocs = dict()

    scoreDocs = []
    for docnum in myresults:
        #doc = searcher.doc(scoreDoc.doc)
        vector = searcher.vector_as("frequency", docnum, content_field)
        #vector = reader.getTermFreqVector(scoreDoc.doc,content_field)
        if vector is None: continue

        d = dict()
        m = dict()
        # a vector is a generator  of tuples -- convert of list
        # [(u"apple", 3), (u"bear", 2), (u"cab", 2)]
        #vector = [elt for elt in vector]            
        #vterms = [elt[0] for elt in vector]
        #vvalues = [elt[1] for elt in vector]
        #allTerms = allTerms.union(map(lambda x: x.encode('utf-8'),vterms))        
#        for (t,num) in zip(vterms,vvalues):
        for (t,num) in vector:
            allTerms.add(t.encode('utf-8'))
            d[t.encode('utf-8')] = num
            if t in termsDocs:
                termsDocs[t.encode('utf-8')] += 1
            else:
                termsDocs[t.encode('utf-8')] = 1
        d["txtorg_id"] = searcher.stored_fields(docnum)["txtorg_id"].encode('utf-8')

        # Build the metadata
        for k in searcher.stored_fields(docnum):
            if k != 'txtorg_id':
                m[k] = searcher.stored_fields(docnum)[k].encode('utf-8')
        allDicts.append(d)
        allMetadata.append(m)
        scoreDocs.append(docnum)
    names = set(allTerms)
    print allMetadata

    return scoreDocs, allTerms, allDicts, termsDocs, allMetadata

def filterDictsTerms(allDicts,allTerms,termsDocs,minDocs,maxDocs):
    import copy

    newDicts = copy.deepcopy(allDicts)
    newTerms = copy.copy(allTerms)

    # each dictionary maps a term to a count
    # we need to count the dictionaries containing a term, and keep track of the terms to remove

    removeTerms = [t for t in termsDocs if (termsDocs[t]<minDocs or termsDocs[t]>maxDocs)]
#    print 'Terms removed because of frequency = ' + str(removeTerms)
    # which terms to remove?
    for d in newDicts:
        for t in removeTerms:
            if t in d:
                d.pop(t)

    return newDicts, newTerms-set(removeTerms)

def writeTDM(allDicts,allTerms,termsDocs,fname,minDocs=0,maxDocs=sys.maxint):
    allDicts, allTerms = filterDictsTerms(allDicts,allTerms,termsDocs,minDocs,maxDocs)
    l = list(allTerms)
    l.sort()
    l = ['txtorg_id']+l

    f = open(fname,'w')
    c = csv.DictWriter(f,l)
    print "writing header"
    dhead = dict()
    for k in l:
        dhead[k] = k
    c.writerow(dhead)
    print "iterating across dictionaries..."
    for d in allDicts:
        c.writerow(d)
    f.close()

def write_CTM_TDM(scoreDocs, allDicts, allTerms,
                  termsDocs, searcher, reader, allMetadata,
                  fname, stm_format = False,minDocs=0,maxDocs=sys.maxint):
    allDicts, allTerms = filterDictsTerms(allDicts,allTerms,termsDocs,minDocs,maxDocs)
    l = list(allTerms)
    l.sort()

    termid_dict = {}
    for termid,term in enumerate(l):
        termid_dict[term] = termid

    # create a filename for the vocab output: tdm.csv -> tdm_vocab.csv
    split_filename_match = re.search(r'(.*)(\.[a-z0-9]+)$',fname)
    vocab_filename = split_filename_match.group(1) + '_vocab' + split_filename_match.group(2)
    md_filename = split_filename_match.group(1) + '_metadata' + split_filename_match.group(2)

    print 'Writing vocabulary list...'
    # writes vocab list in format 'termid, term'
    vocab_lines = [term for term in l]
    vocab_output = '\n'.join(vocab_lines)
    with codecs.open(vocab_filename, 'w', encoding='UTF-8') as outf:
        outf.write(vocab_output.decode('utf8'))

    print 'Writing TDM...'
    # writes TDM in format 'txtorg_id, numterms, termid1: termcount1, [termid2:termcount2], [...]'
    # or, if stm_format = True, uses format 'numterms termid1:termcount1 termid2:termcount2 [...]'
    tdm_output = []
    for document_dict in allDicts:
        numterms = len(document_dict) - 1
        txtorg_id = document_dict['txtorg_id']
        terms = [str(termid_dict[k]) + ':' + str(document_dict[k]) for k in document_dict.keys() if k != 'txtorg_id']
        if stm_format:
            tdm_output.append(' '.join([str(numterms)] + terms))
        else:
            tdm_output.append(','.join([txtorg_id,str(numterms)] + terms))
    with codecs.open(fname, 'w', encoding='UTF-8') as outf:
        outf.write('\n'.join(tdm_output))

    print 'Writing metadata...'
    # writes metadata in CSV format
    all_ids = [d['txtorg_id'] for d in allDicts]

    
    write_metadata(allMetadata, md_filename)    

def write_metadata(allMetadata, fname):
    #fields = sorted(allDicts[0].keys())
    #fields = [u'name',u'path'] + sorted([x for x in allFields if x not in ['name','path']])

    fields = allMetadata[0].keys()
    with codecs.open(fname, 'w', encoding='UTF-8') as outf:
        dw = DictUnicodeWriter(outf, fields)

        # writing header
        dhead = dict()
        for k in fields:
            dhead[k] = k
        dw.writerow(dhead)

        # writing data
        for d in allMetadata:
            dw.writerow(d)

def write_contents(allDicts, searcher, reader, fname, content_field = "contents"):
    all_ids = [d['txtorg_id'] for d in allDicts]

    all_fields = set()
    doc_fields = []
    for txtorg_id in all_ids:
        query = TermQuery(Term('txtorg_id',txtorg_id))
        scoreDocs = searcher.search(query, reader.maxDoc()).scoreDocs
        assert len(scoreDocs) == 1
        scoreDoc = scoreDocs[0]
        doc = searcher.doc(scoreDoc.doc)
        df = {}
        name_path_present = False
        failFlag = False
        for f in doc.getFields():
            field = Field.cast_(f)
            if content_field == "contents" and field.name() == 'path':
                name_path_present = True
                path = doc.get("path").encode('utf-8')
                try:
                    i = codecs.open(path, 'r', encoding='UTF-8')
                    c = i.read()
                    df[content_field] = c
                    i.close()
                except Exception as e:
                    failFlag = True
                    print "Failed for path %s with exception %s" % (path, e)
            elif field.name() in ['txtorg_id', 'name', 'path', content_field]:
                df[field.name()] = field.stringValue()

        all_fields = all_fields.union(set(df.keys()))
        doc_fields.append(df)

    fields = ['txtorg_id'] + sorted([x for x in all_fields if x != 'txtorg_id'])
    with codecs.open(fname, 'w', encoding='UTF-8') as outf:
        dw = csv.DictWriter(outf, fields)
        dw.writeheader()

        # writing data
        for d in doc_fields:
            dw.writerow(d)

    return failFlag


def write_files(searcher,scoreDocs,outdir):

    failFlag = False

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        path = doc.get("path").encode('utf-8')
        try:
            copy2(path,outdir)
            print "Copied:",path
        except:
            failFlag = True
            print "Failed:",path

    if failFlag:
        "WARNING: some files failed to copy."

def print_all_files(reader):
    for i in xrange(reader.maxDoc()):
        if reader.isDeleted(i): continue
        doc = reader.document(i)
        if not os.path.isfile(doc.get("path")):
            print "%s is not a file" % (doc.get("path"),)
