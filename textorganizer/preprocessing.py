#!/usr/bin/env python
# This script hold the various preprocessing functions. They fold into indexfiles (for importing whole docs) or 
# addmetadata (for importing from a CSV)

import chardet
import re, collections

def preprocess(contents, args_dir):
    processed_contents = convert_encodings(contents, args_dir)
    processed_contents = dictionary_replace(processed_contents, args_dir) 
    if args_dir['autocorrect'] == 1:
        import spellchecker # This is burried here because the script reads in the training 
                            # set, and that's super slow (so we don't want to do it if we don't have to)
        processed_contents = automated_english_spellcheck(processed_contents, args_dir) 
    processed_contents = custom_script(processed_contents, args_dir) 
    
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

def dictionary_replace(contents, args_dir):
    return(contents)
 #    if args_dir['autocorrect'] == '1':
        

#     else:
#         tokens = re.findall(r"[\w']+|[.,!?;]", contents)
#         for t in tokens:
            
#         return(' '.join(tokens))

###################
###################

def custom_script(contents, args_dir):
    print(type(args_dir['select_script']))
    print(args_dir['select_script'].get())
    if(type(args_dir['select_script']) == str):
        script = args_dir['select_script']
        execfile(script)
        contents = custom(contents)
        return(contents)
    else:
        return(contents)
