#!/usr/bin/env python
# This script hold the various preprocessing functions. They fold into indexfiles (for importing whole docs) or 
# addmetadata (for importing from a CSV)

import chardet, re, collections

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
    if type(args_dir['dict_filename']) == str:

        dict_filename = args_dir['dict_filename']
        replace_dict = {}
        with open(dict_filename, 'rb') as csvfile:
            cr = csv.reader(csvfile)
            for row in cr:    
                replace_dict[row[0].lower()] = row[1].lower()

        if args_dir['simple_replace'] == 1:
            contents = replace_all(contents, replace_dict)
            return(contents)

        else: # if simple_replace != 1
            pattern = re.compile(r'\b(' + '|'.join(replace_dict.keys()) + r')\b')
            contents = pattern.sub(lambda x: replace_dict[x.group()], contents) # replaces whole words only
            return(contents)
        
    else: # if dict_filename isn't a string
        return(contents)
        
    return(contents)

###################
###################

def custom_script(contents, args_dir):
    if(type(args_dir['script_filename']) == str):
        script = args_dir['script_filename']
        execfile(script)
        contents = custom(contents)
        return(contents)
    else:
        return(contents)

######################
######################
# ASSORTED FUNCTIONS #
######################
######################

def replace_all(text, dic):
    for i, j in dic.iteritems():
            text = text.replace(i,j)
    return text
