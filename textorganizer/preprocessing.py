#!/usr/bin/env python
# This script hold the various preprocessing functions. They fold into indexfiles (for importing whole docs) or 
# addmetadata (for importing from a CSV)

import chardet
import re, collections

'encodings': self.encodings.get(), 

'dict_filename':self.dict_filename, 

'autocorrect':self.auto_correct.get(), 

'smart_correct':self.smart_correct.get()})

def preprocess(contents, args_dir):
    processed_contents = convert_encodings(contents, args_dir)
    processed_contents = dictionary_replace(processed_contents, args_dir) 
    processed_contents = automated_english_spellcheck(processed_contents, args_dir) 
    
    return(processed_contents)

###################
###################

def convert_encodings(contents, args_dir):
    if args_dir['encodings'] == 'DETECT':
        encoding = chardet.detect(contents)['encoding']
        if encoding != 'utf-8':
            contents = contents.decode(encoding, 'replace').encode('utf-8')
    else:
        contents = contents.decode(args_dir['encodings'], 'replace').encode('utf-8')
    
    return(contents)

###################
###################

def dictionary_replacement(contents, args_dir):
    if args_dir['autocorrect'] == '1':
        

    return(contents)

###################
###################

def automated_english_spellcheck(contents, args_dir):
    if args_dir['encodings'] == 'DETECT':
        tokens = re.findall(r"[\w']+|[.,!?;]", contents)
        for t in tokens:
            tokens[t] = correct(tokens[t])
        return(' '.join(tokens))

# Copied this from Peter Norvig
def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('training_text.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
