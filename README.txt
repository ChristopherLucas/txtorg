IMPORTANT NOTE
==================
This README applies to an older command-line only version of txtorg. A full-featured GUI is currently in development, so please check back in the coming weeks if your are interested in trying out txtorg!

iqss-text-organizer
===================

A simple python-based command line tool designed to make organizing data for textual analysis easy and scalable. Creates an Apache Lucene index to which documents can be added. The user can select documents using Lucene queries. Selected documents can be exported in their original format or as a term-document matrix.

SETUP
----------

To use this program, clone the git repository into a directory on your computer and then add the directory to your PATH environment variable. On Ubuntu, this means editing your .bashrc file to contain the line 

export PATH=/path/to/iqss-text-organizer:$PATH

Now you can use the command `txtorg` to run the program from anywhere on your computer. It will create the Lucene index in the directory in which it is installed.

To use PyLucene, please see the installation instructions here:
http://lucene.apache.org/pylucene/install.html

USAGE
-----------

### Adding files to the database

From anywhere on your computer, you can run the command `txtorg -a [DIRECTORY]` to add all the files in `DIRECTORY` (and subdirectories) to the database. 

### Adding metadata to files
Once you have imported files to the database, you can add metadata to the files by running `txtorg -c [file.csv]` where `file.csv` is a file containing a list of metadata fields and values for each file. The file should be in the format of `sample_metadata_file.csv` in the root folder of this repository.

Since `txtorg -c` must remove, edit, and re-add each individual document, it can take a long time to run for large corpora. If this is a problem, you can use the command `txtorg -C [file.csv]` instead of `txtorg -a [DIRECTORY]` to do the initial import. This will import each document in the CSV file, as well as the metadata contained.

### Custom Analyzers
Adding files with the command `txtorg -a` or `txtorg -C` will index the documents using the default analyzer. This analyzer is appropriate only for English text, recognizes only one-word tokens, and does not perform any stemming. Various other analyzers are available that allow indexing documents in other languages, or that perform various processing steps like stemming. To import documents using an analyzer other than the default, use the `-n` switch when importing. For instance, `txtorg -n -a .` imports all documents in the current working directory, but it allows the user to choose which analyzer Lucene will use for indexing. Currently available analyzers include:

* StandardAnalyzer (default)
* SmartChineseAnalyzer (use for Chinese text)
* PorterStemmerAnalyzer
  * This analyzer includes all n-grams (phrases) listed in the file `phrases.txt` as tokens for indexing and TDM export. For instance, if `phrases.txt` included the line `Barack Obama`, then exported TDMs would contain a column for `Barack Obama`. Using the default analyzer, this would be split over two columns: `Barack` and `Obama`. To enable this functionality, place the file `phrases.txt`, containing one entry per line, in the same directory as the `txtorg` executable. To search for a phrase, simply call the select function and include the phrase in quotes.
  * This analyzer also performs a Porter Stemming algorithm on all documents so that, for example, the words `document` and `documents` are counted as the same term in the TDM.


### Selecting and exporting files

To run iqss-text-organizer in interactive mode, you can simply run `txtorg` from the command line. At the prompt (> ), you can choose how to subset the data and what to do with the subsetted data. Current supported commands are `select`, `export`, `view`, `analyzer`, and `quit`.

#### select

* `select [QUERY]` --- runs lucene query QUERY on the database, and prints the number of documents selected.
  * To search by a metadata field, use a query of the form `fieldname:value`. Note that since metadata fields are set to NOT_ANALYZED in the Lucene database, this must be an exact-text match,
  * If you have already made a selection, running `select` again will search within your previous selection. If you want to start a fresh search instead, type `clear` to clear the active selection.

#### Query Syntax (from lucene.apache.org)
Any valid lucene query may be used with `select`. Below are some syntax rules for lucene queries. 
* Boolean operators --- Lucene supports `AND`, `+`, `OR`, `NOT` and `-`(Note: Boolean operators must be ALL CAPS). 
  * `OR` --- links two terms and finds a matching document if either of the terms exist in a document. This is equivalent to a union using sets. The symbol || can be used in place of the word OR.
  * `AND` --- matches documents where both terms exist anywhere in the text of a single document. This is equivalent to an intersection using sets. The symbol && can be used in place of the word AND.
  * `+` --- requires that the term after the `+` symbol exist somewhere in a the field of a single document.
  * `NOT` --- excludes documents that contain the term after NOT. This is equivalent to a difference using sets. 
  * `-` --- excludes documents that contain the term after the `-` symbol.
* Grouping
  * Parentheses may be used to group clauses to form sub queries. This can be very useful if you want to control the boolean logic for a query. To search for either "jakarta" or "apache" and "website" use the query: `(jakarta OR apache) AND website`
  * Parentheses may also be used to group multiple clauses to a single field. To search for a title that contains both the word "return" and the phrase "pink panther" use the query: `title:(+return +"pink panther")`.
* Escaping Special character - `+ - && || ! ( ) { } [ ] ^ " ~ * ? : \` are treated as special characters. To escape these character, use `\` before the character.
* Wildcard searches --- Lucene supports single and multiple character wildcard searches within single terms (not within phrase queries).
  * To perform a single character wildcard search use the `?` symbol. The single character wildcard search looks for terms that match that with the single character replaced. For example, to search for "text" or "test" you can use the search: `te?t`.
  * To perform a multiple character wildcard search use the `*` symbol. Multiple character wildcard searches looks for 0 or more characters. For example, to search for test, tests or tester, you can use the search: `test*`.
  * You cannot use `?` or `*` as the first character in a query.
* Fuzzy Searches --- Lucene supports fuzzy searches based on the Levenshtein Distance, or Edit Distance algorithm. To do a fuzzy search use the tilde, "~", symbol at the end of a Single word Term. For example to search for a term similar in spelling to "roam" use the fuzzy search: `roam~`. This search will find terms like foam and roams.
* Proximity Searches ---  to do a proximity search use the tilde, `~`, symbol at the end of a Phrase. For example to search for a "apache" and "jakarta" within 10 words of each other in a document use the search: `"jakarta apache"~10`.
* Range Searches --- match documents whose field(s) values are between the lower and upper bound specified by the Range Query. Range Queries can be inclusive or exclusive of the upper and lower bounds. Sorting is done lexicographically.
  * Example: `mod_date:[20020101 TO 20030101]` will find documents whose mod_date fields have values between 20020101 and 20030101, inclusive. 

#### clear
* `clear` --- Clears the active selection.

#### export

* `export files` --- exports the full text of all selected documents to a directory.
* `export tdm` --- exports a term-document matrix for all selected documents. This command creates three files; one containing the TDM in the format `filepath, name, number of terms, term_id1: count1, [term_id2: count2], [...]`, one containing the vocabulary of all selected documents in the format `term_id, term`, and one containing the metadata values of all selected documents.
* `export metadata` --- exports a CSV file containing the metadata values of each selected document

#### view

* `view fields` --- prints the names and values of all defined metadata fields for each of the selected documents.

#### analyzer

* `analyzer` --- prints a list of all available analyzers and allows the user to choose one for use in searching/exporting.

#### reindex

* `reindex` --- rebuilds the Lucene index for the selection using the active analyzer. This is useful if you have added terms to `phrases.txt`, as you can re-run the PorterStemmerAnalyzer on a selection using the new additions.

#### index

* `index` --- prints a list of all available Lucene indices and allows the user to choose one for use. This index remains active until the user changes it again (so adding files with `txtorg -a` or `txtorg -C` will add them to the selected Lucene index). Also provides the option to create and use a new Lucene index.

### Index Maintenance
Since adding the content of all files to the Lucene database would take prohibitively large amounts of disk space, the database stores the filepath of each document instead. If files are moved, renamed, or deleted from the disk, then the index no longer points to the file and various features of `txtorg` will fail. The following commands are designed to help maintain the integrity of the index and avoid broken links.

#### cleanup

* `cleanup` --- runs through the entire index and displays a list of items that no longer point to valid files on disk. Allows the user to delete these items from the index if desired.
