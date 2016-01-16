# -*- coding: utf-8 -*-

## Nielsen Stemmer, based in part on the light10 stemmer

# This is a multi-module stemmer.
#
# The available functions are as follows:
#
# "stem" : does all of the stemming functions in order
#
# "stem_and_count" : does all the stemming functions in order
#     and saves a table that lists the frequency of all words
#     that get reduced to each stem.
#
# "removeNumbers" : takes out both English and Arabic numbers
# 
# "clean" : takes all the junk characters out of arabic text, including
#     punctuation, vowelling, and some other junk characters.
#
# "fixAlifs" : takes the hamzas off of alifs.  Run prior to taking out
#     the stopwords.
#
# "cleanChars" : standardizes the characters to a defined list of arabic
#     characters.  All other characters are deleted.
#
# "removeStopWords" : takes a fixed list of stopwords out of Arabic text;
#     prepositions, pronouns, particles, and connecting words.
#
# "transliterate" : transliterates from arabic characters into English
#     characters.
#
# "rev_transliterate" : transliterates from arabic characters into English
#     characters. 
#
# "removePrefixs" : removes prefixes defined in the light 10 paper
#
# "removeSuffixes" : removes suffixes of verbs, possessives, etc , x=9 y=7

## Get libraries
import re
import os
import codecs
from collections import defaultdict
import time

###########################################################
## package all the stemmer functions together
def stem(dat, clean_chars=True, clean_latin_chars=True, transliteration=True):
    dat = removeNewlineChars(dat)  ## gets rid of \n\r\t\f\v
    dat = removePunctuation(dat)  ## gets rid of punctuation
    dat = removeDiacritics(dat)  ## gets rid of Arabic diacritics
    dat = removeEnglishNumbers(dat)  ## gets rid of English numbers
    dat = removeArabicNumbers(dat)  ## gets rid of Arabic numbers
    dat = removeFarsiNumbers(dat)  ## gets rid of Farsi numbers
    dat = fixAlifs(dat)  ## standardizes different hamzas on alif seats
    if clean_chars:
        dat = cleanChars(dat)  ## removes all unicode chars except Latin chars and Arabic alphabet
    if clean_latin_chars:
        dat = cleanLatinChars(dat)  ## removes all Latin chars
    dat = removeStopWords(dat)   ## removes the stopwords
    dat = removePrefixes(dat)  ## removes prefixes
    dat = removeSuffixes(dat)  ## removes suffixes
    if transliteration:
        dat = transliterate(dat)  ## performs transliteration
    return(dat)


###########################################################
## remove numbers

def removeEnglishNumbers (texts):
    texts = re.sub('\d',' ',texts)
    return(re.sub(' {2,}', ' ', texts))


def removeArabicNumbers (texts):
    texts = re.sub(ur'[\u0660-\u0669]',' ',texts)
    return(re.sub(' {2,}', ' ', texts))

def removeFarsiNumbers (texts):
    texts = re.sub(ur'[\u06f0-\u06f9]',' ',texts)
    return(re.sub(' {2,}', ' ', texts))

    
def removeNumbers (texts):
    texts = removeEnglishNumbers(texts)
    texts = removeArabicNumbers(texts)
    texts = removeFarsiNumbers(texts)
    return texts


###########################################################


###########################################################
## clean out junk characters

def removePunctuation (texts):
    ## replace arabic specific punctuation
    texts = re.sub(ur'\u060c|\u061b|\u061f|\u066c|\u066d|\u06d4|\u06dd|\u06de|\u06e9',' ',texts)
    ## replace other junk characters that sometimes show up
    texts = re.sub(ur'[\u200C-\u200F]|&nbsp|~|\u2018|\u2022|\u2013|\u2026|\u201c|\u201d|\u2019|\ufd3e|\ufd3f',' ',texts)
    texts = re.sub(r'\xbb|\xab|\xf7|\xb7',' ', texts)
    ## remove general punctuation
    texts = re.sub(',|/|`|\$|\.|\^|\*|\+|\?|\{|\|\}|\!|\\|\[|\]|\:|\||\}|\<|\>|\#|\%|\(|\)|\@|\&|\-|_|\=|\[|\\\\|\;|\'|\"',' ',texts)
    return texts
    
def removeDiacritics (texts):
    texts = re.sub(ur'[\u0610-\u061a]|\u0640|[\u064b-\u065f]|\u0670|[\u06d6-\u06dc]|[\u06df-\u06e4]|[\u06e7-\u06e8]|[\u06ea-\u06ed]',' ',texts)
    return(re.sub(' {2,}', ' ', texts))

def removeNewlineChars (texts):
    texts = re.sub('\n|\r|\t|\f|\v',' ', texts)
    return(re.sub(' {2,}', ' ', texts))


## legacy function -- punctuation and diacritics together
def clean (texts):
    texts = removePunctuation(texts)
    texts = removeDiacritics(texts)
    texts = removeNewlineChars(texts)
    return(texts)
    
#######################################################
## Standardize the alifs

def fixAlifs (texts):
    return re.sub(ur'\u0622|\u0623|\u0625|[\u0671-\u0673]|\u0675',ur'\u0627',texts)


#######################################################
## clean up the characters

def cleanChars (texts):
    # http://jrgraphix.net/research/unicode_blocks.php
    ## ones I'm dropping
    texts = re.sub(ur'[\u00A0-\u0600]|[\u0600-\u0621]|[\u063b-\u0640]|[\u064b-\u065f]|[\u066a-\u067d]|[\u0700-\uFB4F]|[\uFB50-\uFDFF]|[\uFE00-\uFFFF]','',texts)
    ## I could sort through these ones too: http://jrgraphix.net/r/Unicode/FB50-FDFF, but I'm not right now
    ## clean up spaces
    return(re.sub(' {2,}', ' ', texts))

def cleanLatinChars (texts):
    texts = re.sub(ur'[a-zA-Z]','',texts)
    ## clean up spaces
    return(re.sub(' {2,}', ' ', texts))
    


#######################################################
## Remove stopwords

def removeStopWords (texts):

    # Split up the words...
    texts_split = texts.split(" ")

    preps = [
        u'\u0641\u064a',  #fy
        u'\u0641\u064a\u0647',  #fyh
        u'\u0641\u064a\u0647\u0627',  #fyha
        u'\u0641\u064a\u0647\u0645',  #fyhm
        u'\u0639\u0644\u0649',  #3lA
        u'\u0639\u0644\u064a\u0643',  #3lyk
        u'\u0639\u0644\u064a\u0647',  #3lyh
        u'\u0639\u0644\u064a\u0647\u0627',  #3lyha
        u'\u0639\u0644\u064a\u0647\u0645',  #3lyhm
        u'\u0639\u0644\u064a',  #3ly
        u'\u0628\u0647',  #bh
        u'\u0628\u0647\u0627',  #bha
        u'\u0628\u0647\u0645',  #bhm
        u'\u0644\u0647',  #lh
        u'\u0644\u0647\u0627',  #lha
        u'\u0644\u0647\u0645',  #lhm
        u'\u0645\u0639',  #m3
        u'\u0645\u0639\u0647',  #m3h
        u'\u0645\u0639\u0647\u0627',  #m3ha
        u'\u0645\u0639\u0647\u0645',  #m3hm
        u'\u0639\u0646',  #3n
        u'\u0639\u0646\u0647',  #3nh
        u'\u0639\u0646\u0647\u0627',  #3nha
        u'\u0639\u0646\u0647\u0645',  #3nhm
        u'\u062a\u062d\u062a',  #t7t
        u'\u062d\u062a\u0649',  #7tA
        u'\u0641\u0648\u0642',  #fwQ
        u'\u0641\u0648\u0642\u064e',  #fwQ?
        u'\u0628\u062c\u0627\u0646\u0628',  #bjanb
        u'\u0623\u0645\u0627\u0645',  #amam
        u'\u0623\u0645\u0627\u0645\u064e',  #amam?
        u'\u0627\u0645\u0627\u0645',  #amam
        u'\u062e\u0627\u0631\u062c',  #Karj
        u'\u0628\u0627\u0644\u062e\u0627\u0631\u062c',  #balKarj
        u'\u062d\u0648\u0644\u064e',  #7wl?
        u'\u062d\u0648\u0644',  #7wl
        u'\u0631\u063a\u0645',  #rGm
        u'\u0628\u0627\u0644\u0631\u063a\u0645',  #balrGm
        u'\u0631\u063a\u0645\u064e',  #rGm?
        u'\u0645\u0646\u0630',  #mni
        u'\u0645\u0646\u0630\u064f',  #mni?
        u'\u0645\u0646',  #mn
        u'\u062e\u0644\u0627\u0644',  #Klal
        u'\u062e\u0644\u0627\u0644\u064e',  #Klal?
        u'\u062d\u0648\u0644',  #7wl
        u'\u062d\u0648\u0644\u064e',  #7wl?
        u'\u0642\u0628\u0644',  #Qbl
        u'\u0642\u0628\u0644\u064e',  #Qbl?
        u'\u0648\u0641\u0642\u0627',  #wfQa
        u'\u0625\u0644\u0649',  #alA
        u'\u0627\u0644\u0649\u0648\u0631\u0627\u0621\u064e',  #alAwraq?
        u'\u0648\u0631\u0627\u0621',  #wraq
        u'\u0628\u064a\u0646\u064e',  #byn?
        u'\u0628\u064a\u0646',  #byn
        u'\u0628\u062f\u0648\u0646',  #bdwn
        u'\u0644\u0643\u0646',  #lkn
        u'\u0628\u0627\u062a\u062c\u0627\u0647',  #batjah
        u'\u0623\u0642\u0644',  #aQl
        u'\u0627\u0642\u0644',  #aQl
        u'\u0627\u0643\u062b\u0631'  #akUr
        ]  

    pronouns = [
        u'\u0647\u0630\u0627',  #hia
        u'\u0647\u0630\u0647',  #hih
        u'\u0630\u0644\u0643',  #ilk
        u'\u062a\u0644\u0643',  #tlk
        u'\u0647\u0624\u0644\u064e\u0627\u0621',  #hol?aq
        u'\u0647\u0624\u0644\u0627\u0621',  #holaq
        u'\u0627\u0648\u0644\u0627\u0626\u0643',  #awla5k
        u'\u0647\u0630\u0627\u0646',  #hian
        u'\u0647\u0630\u064a\u0646\u0647\u062a\u0627\u0646',  #hiynhtan
        u'\u0647\u062a\u064a\u0646\u0623\u0646\u0627',  #htynana
        u'\u0627\u0646\u0627',  #ana
        u'\u0623\u0646\u062a',  #ant
        u'\u0647\u0645\u0627',  #hma
        u'\u0623\u0646\u062a\u064e',  #ant?
        u'\u0627\u0646\u062a',  #ant
        u'\u0623\u0646\u062a',  #ant
        u'\u0623\u0646\u062a\u0650',  #ant?
        u'\u0627\u0646\u062a\u0647\u0648',  #anthw
        u'\u0647\u0648\u064e',  #hw?
        u'\u0647\u0648',  #hw
        u'\u0647\u064a',  #hy
        u'\u0647\u064a\u064e',  #hy?
        u'\u0646\u062d\u0646',  #n7n
        u'\u0623\u0646\u062a\u0645',  #antm
        u'\u0627\u0646\u062a\u0645',  #antm
        u'\u0623\u0646\u062a\u0645',  #antm
        u'\u0627\u0646\u062a\u0645',  #antm
        u'\u0647\u064f\u0645',  #h?m
        u'\u0647\u0645',  #hm
        u'\u0644\u0647\u0645',  #lhm
        u'\u0645\u0646\u0647\u0645',  #mnhm
        u'\u0648\u0647\u0645',  #whm
        u'\u0627\u0644\u062a\u064a',  #alty
        u'\u0627\u0644\u0630\u064a',  #aliy
        u'\u0627\u0644\u0644\u0630\u0627\u0646',  #allian
        u'\u0627\u0644\u0644\u0630\u064a\u0646',  #alliyn
        u'\u0627\u0644\u0644\u062a\u0627\u0646',  #alltan
        u'\u0627\u0644\u0644\u062a\u064a\u0646'  #alltyn
        ]

    particles = [
        u'\u0627\u0646',  #an
        u'\u0648\u0627\u0646',  #wan
        u'\u0625\u0646',  #an
        u'\u0625\u0646\u0647',  #anh
        u'\u0625\u0646\u0647\u0627',  #anha
        u'\u0625\u0646\u0647\u0645',  #anhm
        u'\u0625\u0646\u0647\u0645\u0627',  #anhma
        u'\u0625\u0646\u064a',  #any
        u'\u0648\u0625\u0646',  #wan
        u'\u0648\u0623\u0646',  #wan
        u'\u0627\u0646',  #an
        u'\u0627\u0646\u0647',  #anh
        u'\u0627\u0646\u0647\u0627',  #anha
        u'\u0627\u0646\u0647\u0645',  #anhm
        u'\u0627\u0646\u0647\u0645\u0627',  #anhma
        u'\u0627\u0646\u064a',  #any
        u'\u0648\u0627\u0646',  #wan
        u'\u0648\u0627\u0646',  #wan
        u'\u0623\u0646',  #an
        u'\u0627\u0646',  #an
        u'\u0623\u0644\u0627',  #ala
        u'\u0628\u0623\u0646',  #ban
        u'\u0627\u0646',  #an
        u'\u0627\u0644\u0627',  #ala
        u'\u0628\u0627\u0646',  #ban
        u'\u0623\u0646\u0647',  #anh
        u'\u0623\u0646\u0647\u0627',  #anha
        u'\u0623\u0646\u0647\u0645',  #anhm
        u'\u0623\u0646\u0647\u0645\u0627',  #anhma
        u'\u0627\u0646\u0647',  #anh
        u'\u0627\u0646\u0647\u0627',  #anha
        u'\u0627\u0646\u0647\u0645',  #anhm
        u'\u0627\u0646\u0647\u0645\u0627',  #anhma
        u'\u0623\u0630',  #ai
        u'\u0627\u0630',  #ai
        u'\u0627\u0630\u0627',  #aia
        u'\u0625\u0630',  #ai
        u'\u0625\u0630\u0627',  #aia
        u'\u0648\u0625\u0630',  #wai
        u'\u0648\u0625\u0630\u0627',  #waia
        u'\u0627\u0630',  #ai
        u'\u0627\u0630',  #ai
        u'\u0627\u0630\u0627',  #aia
        u'\u0627\u0630',  #ai
        u'\u0627\u0630\u0627',  #aia
        u'\u0641\u0627\u0630\u0627',  #faia
        u'\u0645\u0627\u0630\u0627',  #maia
        u'\u0648\u0627\u0630',  #wai
        u'\u0648\u0627\u0630\u0627',  #waia
        u'\u0644\u0648\u0644\u0627',  #lwla
        u'\u0644\u0648',  #lw
        u'\u0648\u0644\u0648\u0633\u0648\u0641',  #wlwswf
        u'\u0644\u0646',  #ln
        u'\u0645\u0627',  #ma
        u'\u0644\u0645',  #lm
        u'\u0648\u0644\u0645',  #wlm
        u'\u0623\u0645\u0627',  #ama
        u'\u0627\u0645\u0627',  #ama
        u'\u0644\u0627',  #la
        u'\u0625\u0644\u0627',  #ala
        u'\u0627\u0644\u0627',  #ala
        u'\u0623\u0645',  #am
        u'\u0623\u0648',  #aw
        u'\u0627\u0645',  #am
        u'\u0627\u0648',  #aw
        u'\u0628\u0644',  #bl
        u'\u0623\u0646\u0645\u0627',  #anma
        u'\u0625\u0646\u0645\u0627',  #anma
        u'\u0628\u0644',  #bl
        u'\u0627\u0646\u0645\u0627',  #anma
        u'\u0627\u0646\u0645\u0627',  #anma
        u'\u0648'  #w
        ]

    # Connectors
    connectors = [u'\u0628\u0645\u0627',  #bma
        u'\u0643\u0645\u0627',  #kma
        u'\u0644\u0645\u0627',  #lma
        u'\u0644\u0623\u0646',  #lan
        u'\u0644\u064a', #ly
        u'\u0644\u0649', #ly
        u'\u0644\u0623\u0646\u0647',  #lanh
        u'\u0644\u0623\u0646\u0647\u0627',  #lanha
        u'\u0644\u0623\u0646\u0647\u0645',  #lanhm
        u'\u0644\u0627\u0646',  #lan
        u'\u0644\u0627\u0646\u0647',  #lanh
        u'\u0644\u0627\u0646\u0647\u0627',  #lanha
        u'\u0644\u0627\u0646\u0647\u0645',  #lanhm
        u'\u062b\u0645',  #Um
        u'\u0623\u064a\u0636\u0627',  #ayDa
        u'\u0627\u064a\u0636\u0627',  #ayDa
        u'\u0643\u0630\u0644\u0643',  #kilk
        u'\u0642\u0628\u0644',  #Qbl
        u'\u0628\u0639\u062f',  #b3d
        u'\u0644\u0643\u0646',  #lkn
        u'\u0648\u0644\u0643\u0646',  #wlkn
        u'\u0644\u0643\u0646\u0647',  #lknh
        u'\u0644\u0643\u0646\u0647\u0627',  #lknha
        u'\u0644\u0643\u0646\u0647\u0645',  #lknhm
        u'\u0641\u0642\u0637',  #fQT
        u'\u0631\u063a\u0645',  #rGm
        u'\u0628\u0627\u0644\u0631\u063a\u0645',  #balrGm
        u'\u0628\u0641\u0636\u0644',  #bfDl
        u'\u062d\u064a\u062b',  #7yU
        u'\u0628\u062d\u064a\u062b',  #b7yU
        u'\u0644\u0643\u064a',  #lky
        u'\u0647\u0646\u0627',  #hna
        u'\u0647\u0646\u0627\u0643',  #hnak
        u'\u0628\u0633\u0628\u0628',  #bsbb
        u'\u0630\u0627\u062a',  #iat
        u'\u0630\u0648',  #iw
        u'\u0630\u064a',  #iy
        u'\u0630\u0649',  #iy
        u'\u0648\u0647', #wh
        u'\u064a\u0627',  #ya
        u'\u0627\u0646\u0645\u0627',  #anma
        u'\u0641\u0647\u0630\u0627',  #fhia
        u'\u0641\u0647\u0648',  #fhw
        u'\u0641\u0645\u0627',  #fma
        u'\u0641\u0645\u0646',  #fmn
        u'\u0641\u064a\u0645\u0627', #fyma
        u'\u0641\u0647\u0644',  #fhl
        u'\u0648\u0647\u0644',  #fhl
        u'\u0641\u0647\u0624\u0644\u0627\u0621',  #fholaq
        u'\u0643\u0630\u0627', #kia
        u'\u0644\u0630\u0644\u0643', #lilk
        u'\u0644\u0645\u0627\u0630\u0627', #lmaia
        u'\u0644\u0645\u0646', #lmn
        u'\u0644\u0646\u0627',  #lna
        u'\u0645\u0646\u0627',  #mna
        u'\u0645\u0646\u0643',  #mnk
        u'\u0645\u0646\u0643\u0645',  #mnkm
        u'\u0645\u0646\u0647\u0645\u0627',  #mnhma
        u'\u0644\u0643', #lk
        u'\u0648\u0644\u0648', #wlw
        u'\u0645\u0645\u0627', #mma
        u'\u0639\u0646\u062f',  #3nd
        u'\u0639\u0646\u062f\u0647\u0645',  #3ndhm
        u'\u0639\u0646\u062f\u0645\u0627',  #3ndma
        u'\u0639\u0646\u062f\u0646\u0627',  #3ndna
        u'\u0639\u0646\u0647\u0645\u0627',  #3nhma
        u'\u0639\u0646\u0643',  #3nk
        u'\u0627\u0630\u0646',  #ain
        u'\u0627\u0644\u0630\u064a',  #aliy
        u'\u0641\u0627\u0646\u0627',  #fana
        u'\u0641\u0627\u0646\u0647\u0645',  #fanhm
        u'\u0641\u0647\u0645',  #fhm
        u'\u0641\u0647',  #fh
        u'\u0641\u0643\u0644',  #fkl
        u'\u0644\u0643\u0644',  #lkl
        u'\u0644\u0643\u0645',  #lkm
        u'\u0641\u0644\u0645',  #flm
        u'\u0641\u0644\u0645\u0627',  #flma
        u'\u0641\u064a\u0643',  #fyk
        u'\u0641\u064a\u0643\u0645',  #fykm
        u'\u0644\u0647\u0630\u0627'    # lhia
        ]

    all = preps+pronouns+particles+connectors
    all = ' '.join(all)
    all = all+ ' ' + fixAlifs(all)
    all = list(set(all.split(' ')))
    
    for i in range(len(texts_split)):
        word = texts_split[i] 
        if word in all :
            texts_split[i] = ''

    # Rejoining the texts again...
    texts = ''.join([word + " "  for word in texts_split])
    # split to get rid of white space
    #texts_split = new_texts.split()
    # then re-rejoin them.
    #out_texts = ''.join([word + " "  for word in texts_split])
    ## clean up spaces
    return(re.sub(' {2,}', ' ', texts))


#######################################################
## Transliterate from arabic to english

def transliterate(texts):

    text_alter = texts   

    # The alphabet 
    text_alter = text_alter.replace(unicode('ا', encoding='utf-8'), 'a')
    text_alter = text_alter.replace(unicode('ى', encoding='utf-8'), 'A')
    text_alter = text_alter.replace(unicode('ب', encoding='utf-8'), 'b')
    text_alter = text_alter.replace(unicode('ت', encoding='utf-8'), 't')
    text_alter = text_alter.replace(unicode('ث', encoding='utf-8'), 'U')
    text_alter = text_alter.replace(unicode('ج', encoding='utf-8'), 'j')
    text_alter = text_alter.replace(unicode('ح', encoding='utf-8'), '7')
    text_alter = text_alter.replace(unicode('خ', encoding='utf-8'), 'K')
    text_alter = text_alter.replace(unicode('د', encoding='utf-8'), 'd')
    text_alter = text_alter.replace(unicode('ذ', encoding='utf-8'), 'i')
    text_alter = text_alter.replace(unicode('ر', encoding='utf-8'), 'r')
    text_alter = text_alter.replace(unicode('ز', encoding='utf-8'), 'z')
    text_alter = text_alter.replace(unicode('س', encoding='utf-8'), 's')
    text_alter = text_alter.replace(unicode('ش', encoding='utf-8'), 'W')
    text_alter = text_alter.replace(unicode('ص', encoding='utf-8'), 'S')
    text_alter = text_alter.replace(unicode('ض', encoding='utf-8'), 'D')
    text_alter = text_alter.replace(unicode('ط', encoding='utf-8'), 'T')
    text_alter = text_alter.replace(unicode('ظ', encoding='utf-8'), 'Z')
    text_alter = text_alter.replace(unicode('ع', encoding='utf-8'), '3')
    text_alter = text_alter.replace(unicode('غ', encoding='utf-8'), 'G')
    text_alter = text_alter.replace(unicode('ف', encoding='utf-8'), 'f')
    text_alter = text_alter.replace(unicode('ق', encoding='utf-8'), 'Q')
    text_alter = text_alter.replace(unicode('ك', encoding='utf-8'), 'k')
    text_alter = text_alter.replace(unicode('ل', encoding='utf-8'), 'l')
    text_alter = text_alter.replace(unicode('م', encoding='utf-8'), 'm')
    text_alter = text_alter.replace(unicode('ن', encoding='utf-8'), 'n')
    text_alter = text_alter.replace(unicode('ه', encoding='utf-8'), 'h')
    text_alter = text_alter.replace(unicode('و', encoding='utf-8'), 'w')
    text_alter = text_alter.replace(unicode('ي', encoding='utf-8'), 'y')
    # Hamzas
    text_alter = text_alter.replace(unicode('أ', encoding='utf-8'), 'a')
    text_alter = text_alter.replace(unicode('إ', encoding='utf-8'), 'a')
    text_alter = text_alter.replace(unicode('ؤ', encoding='utf-8'), 'o')
    text_alter = text_alter.replace(unicode('ئ', encoding='utf-8'), '5')
    text_alter = text_alter.replace(unicode('ء', encoding='utf-8'), 'q')
    text_alter = text_alter.replace(unicode('آ', encoding='utf-8'), 'a')
    # taa-marbuta and other special letters
    text_alter = text_alter.replace(unicode('ة', encoding='utf-8'), '0')

    # Rare Characters
    text_alter = text_alter.replace(u'\u067E', 'p')  # Arabic "peh" -- ba with three dots
    text_alter = text_alter.replace(u'\u06C1', 'h')  # another version of heh
    text_alter = text_alter.replace(u'\u06A9', 'k')  # another version of kaf, called keheh
    text_alter = text_alter.replace(u'\u0679', 't')  # a taa with a Taa over it?
    text_alter = text_alter.replace(u"\u06BA", 'n')  # a noon without a dot?
    text_alter = text_alter.replace(u"\u06D2", 'y')  # a weird yeh
    text_alter = text_alter.replace(u'\u06cc', 'y')  # ARABIC LETTER DOTLESS YA
    text_alter = text_alter.replace(u"\u0671", 'a')  # ARABIC LETTER DOTLESS YA
    text_alter = text_alter.replace(u"\ufedf", 'l')  # http://www.webtoolhub.com/tn561380-xhtml-characters-list.aspx?type=script&category=arabic-form-b
    text_alter = text_alter.replace(u"\uFEEB", 'h')  # http://www.webtoolhub.com/tn561380-xhtml-characters-list.aspx?type=script&category=arabic-form-b
    text_alter = text_alter.replace(u"\u063f", 'y')  # (special three dot yeh) http://www.marathon-studios.com/unicode/U063F/Arabic_Letter_Farsi_Yeh_With_Three_Dots_Above
    text_alter = text_alter.replace(u"\u063d", 'y')  # special yah: http://www.marathon-studios.com/unicode/U063D/Arabic_Letter_Farsi_Yeh_With_Inverted_V
    text_alter = text_alter.replace(u"\u063e", 'y')  # special yah
    text_alter = text_alter.replace(u"\u063b", 'k')  # keheh with dots
    text_alter = text_alter.replace(u"\u063c", 'k')  # keheh with dots

    return text_alter


#######################################################
## Transliterate from English to Arabic

def rev_transliterate(texts):

    text_alter = texts   

    # The alphabet 
    text_alter = text_alter.replace('a', unicode('ا', encoding='utf-8'))
    text_alter = text_alter.replace('A', unicode('ى', encoding='utf-8'))
    text_alter = text_alter.replace('b', unicode('ب', encoding='utf-8'))
    text_alter = text_alter.replace('t', unicode('ت', encoding='utf-8'))
    text_alter = text_alter.replace('U', unicode('ث', encoding='utf-8'))
    text_alter = text_alter.replace('j', unicode('ج', encoding='utf-8'))
    text_alter = text_alter.replace('7', unicode('ح', encoding='utf-8'))
    text_alter = text_alter.replace('K', unicode('خ', encoding='utf-8'))
    text_alter = text_alter.replace('d', unicode('د', encoding='utf-8'))
    text_alter = text_alter.replace('i', unicode('ذ', encoding='utf-8'))
    text_alter = text_alter.replace('r', unicode('ر', encoding='utf-8'))
    text_alter = text_alter.replace('z', unicode('ز', encoding='utf-8'))
    text_alter = text_alter.replace('s', unicode('س', encoding='utf-8'))
    text_alter = text_alter.replace('W', unicode('ش', encoding='utf-8'))
    text_alter = text_alter.replace('S', unicode('ص', encoding='utf-8'))
    text_alter = text_alter.replace('D', unicode('ض', encoding='utf-8'))
    text_alter = text_alter.replace('T', unicode('ط', encoding='utf-8'))
    text_alter = text_alter.replace('Z', unicode('ظ', encoding='utf-8'))
    text_alter = text_alter.replace('3', unicode('ع', encoding='utf-8'))
    text_alter = text_alter.replace('G', unicode('غ', encoding='utf-8'))
    text_alter = text_alter.replace('f', unicode('ف', encoding='utf-8'))
    text_alter = text_alter.replace('Q', unicode('ق', encoding='utf-8'))
    text_alter = text_alter.replace('k', unicode('ك', encoding='utf-8'))
    text_alter = text_alter.replace('l', unicode('ل', encoding='utf-8'))
    text_alter = text_alter.replace('m', unicode('م', encoding='utf-8'))
    text_alter = text_alter.replace('n', unicode('ن', encoding='utf-8'))
    text_alter = text_alter.replace('h', unicode('ه', encoding='utf-8'))
    text_alter = text_alter.replace('w', unicode('و', encoding='utf-8'))
    text_alter = text_alter.replace('y', unicode('ي', encoding='utf-8'))

    # Hamzas
    text_alter = text_alter.replace('o', unicode('ؤ', encoding='utf-8'))
    text_alter = text_alter.replace('5', unicode('ئ', encoding='utf-8'))
    text_alter = text_alter.replace('q', unicode('ء', encoding='utf-8'))
    # taa-marbuta and other special letters
    text_alter = text_alter.replace('0', unicode('ة', encoding='utf-8')) 

    # Rare Characters
    text_alter = text_alter.replace('p', u'\u067E')  # Arabic "peh" -- ba with three dots

    return text_alter


############################################################
## This removes the "prefixes" in light 10

def removePrefixes (texts, x1=4, x2=4, x3=5, x4=5, x5=5,
                      x6=5, x7=4):

    # Note that I only allow one prefix to be taken off each word

    # Split up the words...
    texts_split = texts.split(" ")

    for i in range(len(texts_split)):
        word = texts_split[i]

        ## a list of words to not stem
        if not word in [u'الله',u'لله']:
                
            if len(word) >= x2 : 
                if word.startswith(u'ال'):
                    texts_split[i] = word.replace(u'ال', '', 1)
                    continue
                
            if len(word) >= x3 : 
                if word.startswith(u'وال'):
                    texts_split[i] = word.replace(u'وال', '', 1)
                    continue
                
            if len(word) >= x4 :
                if word.startswith(u'بال'):
                    texts_split[i] = word.replace(u'بال', '', 1)
                    continue
                
            if len(word) >= x5 :
                if word.startswith(u'كال'):
                    texts_split[i] = word.replace(u'كال', '', 1)
                    continue
                
            if len(word) >= x6 :
                if word.startswith(u'فال'):
                    texts_split[i] = word.replace(u'فال', '', 1)
                    continue

            if len(word) >= x7 :
                if word.startswith(u'لل'):                        
                    texts_split[i] = word.replace(u'لل', '', 1)
                    continue

            if len(word) >= x1 : 
                if word.startswith(u'و'):
                    texts_split[i] = word.replace(u'و', '', 1)
                    continue

    # Rejoining the texts again...
    out_texts = ''.join([word + " "  for word in texts_split])
    # split to get rid of white space
    texts_split = out_texts.split()
    # then re-rejoin them.
    out_texts = ''.join([word + " "  for word in texts_split])

    return out_texts

############################################################



############################################################
## remove suffixes, in the order described in the light 10 paper

def removeSuffixes(texts, x1=4, x2=4, x3=4, x4=4, x5=4, x6=4, x7=4, x8=3, x9=3, x10=3):

    # Note that I only allow one suffix to be taken off each word

    # Split up the words...
    texts_split = texts.split(" ")
         
    for i in range(len(texts_split)):
        word = texts_split[i]

        ## a list of words to not stem
        if not word in [u'الله',u'لله']:
            
            if len(word) >= x1: 
                if word.endswith(u'ها'):
                    texts_split[i] = word[0:-2]
                    continue
                    
            if len(word) >= x2: 
                if word.endswith(u'ان'):
                    texts_split[i] = word[0:-2]
                    continue

            if len(word) >= x3: 
                if word.endswith(u'ات'):
                    texts_split[i] = word[0:-2]
                    continue

            if len(word) >= x4: 
                if word.endswith(u'ون'):
                    texts_split[i] = word[0:-2]
                    continue

            if len(word) >= x5: 
                if word.endswith(u'ين'):
                    texts_split[i] = word[0:-2]
                    continue

            if len(word) >= x6: 
                if word.endswith(u'يه'):
                    texts_split[i] = word[0:-2]
                    continue

            if len(word) >= x7: 
                if word.endswith(u'ية'):
                    texts_split[i] = word[0:-2]
                    continue

            if len(word) >= x8: 
                if word.endswith(u'ه'):
                    texts_split[i] = word[0:-1]
                    continue

            if len(word) >= x9: 
                if word.endswith(u'ة'):
                    texts_split[i] = word[0:-1]
                    continue

            if len(word) >= x10: 
                if word.endswith(u'ي'):
                    texts_split[i] = word[0:-1]
                    continue          

    # Rejoining the texts again...
    out_texts = ''.join([word + " "  for word in texts_split])
    # split to get rid of white space
    texts_split = out_texts.split()
    # then re-rejoin them.
    out_texts = ''.join([word + " "  for word in texts_split])

    return out_texts

#####################################################


