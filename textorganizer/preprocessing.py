#!/usr/bin/env python
# This script hold the various preprocessing functions. Most of them find their way into the workflow in indexfiles.py.
# Email Chris for questions
import chardet

'encodings': self.encodings.get(), 

'dict_filename':self.dict_filename, 

'autocorrect':self.auto_correct.get(), 

'smart_correct':self.smart_correct.get()})

def preprocess(contents, args_dir):
    processed_contents = convert_encodings(contents, args_dir)
    processed_contents = dictionary_replace(processed_contents, args_dir) 
    processed_contents = automated_english_spellcheck(processed_contents, args_dir) 
    
    return(processed_contents)

def convert_encodings(contents, args_dir):
    if args_dir['encodings'] == 'DETECT':
        encoding = chardet.detect(contents)['encoding']
        if encoding != 'utf-8':
            contents = contents.decode(encoding, 'replace').encode('utf-8')
    else:
        contents = contents.decode(args_dir['encodings'], 'replace').encode('utf-8')
    
    return(contents)

def dictionary_replacement(contents, args_dir):
    

def automated_english_spellcheck(contents, args_dir):
    
