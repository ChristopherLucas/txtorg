#!/usr/bin/env python
import argparse
from argparse import ArgumentParser
import os.path
import csv 
import string 

# TASK DESCRIPTION
# This command line utility diagnoses and fixes errors in corpora to be imported into txtorg. 

# Some functions 
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
       parser.error("The file %s does not exist!"%arg)
    else:
       return open(arg,'r')  #return an open file handle

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def removeNonAscii(s): 
	return "".join(i for i in s if ord(i)<128)

# Create the parser
parser = ArgumentParser(description="Diagnose and repair errors in corpora for import into txtorg")    
parser.add_argument("--csv", dest="csv_filename", required=False,
    help="input csv", metavar = "csv file",
    type=lambda x: is_valid_file(parser,x))
parser.add_argument("--dictionary", dest="dict_filename", required=False,
    help="input dictionary", metavar = "dictionary file",
    type=lambda x: is_valid_file(parser,x))
parser.add_argument('-e', help = 'encodings flag', action='store_true', dest = 'encoding_flag')
parser.add_argument('--outfile', dest='out_filename', type=argparse.FileType('w'), 
                    required=True, help = 'output file', 
                    metavar = 'output filename')

args = parser.parse_args()
print(args)
# Read the replacement dict with content
if args.dict_filename != None:
    replace_dict = {}
    cr = csv.reader(args.dict_filename)
    for row in cr:    
        replace_dict[row[0]] = row[1]
 
# Read csv with content
if args.csv_filename != None:
    csvWithContent = []
    cr = csv.reader(args.csv_filename)
    for row in cr:    
        if args.dict_filename != None:
            row = [replace_all(element, replace_dict) for element in row]
        if args.encoding_flag:
            row = [removeNonAscii(element) for element in row]
        csvWithContent.append(row)

# write csv
with args.out_filename as filename:
  file_writer = csv.writer(filename)
  for row in csvWithContent:
    file_writer.writerow(row)
