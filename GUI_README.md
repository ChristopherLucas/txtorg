This readme is for the GUI version of txtorg.

Getting Started
==============

Installation
--------------

Install the package as you would any other Python package (PyPI, Distutils, etc). For example...

1. Navigate to the directory in which you cloned the repo. This should contain setup.py.

2. Enter 'python setup.py install'

Launching Txtorg
--------------

From the command line, enter 'txtorg'

Using Txtorg
==============

Loading your corpus
--------------

1. Create a new corpus. To do so, click File -> New Corpus. You'll be prompted to select a place to store the corpus.

2. The corpus should show up in the corpus window. Now select your corpus by clicking on it.

3. Next, import some documents. With your corpus highlighted, click Corpus -> Import Documents. Next, select the format of your corpus. We support several different corpus options described below.

- To import all the documents in a directory (a folder), select 'Import an entire directory'. These must be .txt files. In this case, you do not have any metadata about the documents that you are uploading. 

- To import documents from a .csv with a field containing the filepaths of all the documents in the corpus, select 'Import from a CSV file (not including content)'. Then select the field containing the filepaths. brothersk_without_content.csv, in the examples directory, is an example of one such csv. 

- To import documents from a .csv with a field containing the full documents, select 'Import from a CSV file (including content)'. Then select the field containing the documents. brothersk_with_content.csv, in the examples directory, is an example of one such csv.

NOTE: If you want to import metadata for your documents, you must import the documents from a csv containing content. The content field is uploaded as the docs, while the remaining fields are uploaded as metadata. [Chris this is not clear. We need to describe above, for both the mturk style csv and for the other version how to deal w metadata]

Getting a TDM
--------------

1. The documents should be imported already. If not, see the previous section. 

2. Now pick your analyzer. Corpus -> Change Analyzer. Just click on the analyzer you want and then click OK. To see the difference between the different analyzers, enter text in the sample window, and select an analyzer. The tokens output by that analzyer will appear in the main window.

3. Now rebuild the index file by clicking Corpus -> Rebuild Index File.

4. Now select docs. To select all the docs in the corpus, search for 'all'. To subset, use a valid Lucene query.

5. To export the tdm for the selected docs, click Export TDM. Then select the format.

- STM format will write a TDM, metadata file, and vocab list. The tdm will be in the format '[M] [term_1]:[count_1] [term_2]:[count_2] ... [term_N]:[count_3]', where [M] is the number of unique terms in the document, [term_i] is an integer associated with the i-th term in the vocabulary, and [count_i] is how many times the i-th term appeared in the document. This is the most common format.

- CTM format will be the same as STM format, except it will be delimited by commas and will include a field for the lucene ID.

- Flat CSV will export a TDM, metadata file, and vocab list. The tdm will be a flat csv, with lots of zeros.


Notes and Potential Problems/Solutions
==============

1. If you are unable to export a tdm, check the directory containing the Lucene index for a final 'write.locked'. If it contains such a file, delete it and try again. If that doesn't work, try reuploading the docs to a new corpus. 
