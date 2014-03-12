<?php include 'php/header.php'; ?>
<section>
  <h1>
    <a name="welcome-to-txtorg" class="anchor" href="#welcome-to-txtorg"><span class="octicon octicon-link"></span></a>Index-based text management</h1>
  
  <p>txtorg is a Python-based utility that leverages Apache Lucene to facilitate text preprocessing and management. It outputs processed text 
    in a variety of formats for use in a wide array of analytical software, including (but not limited to) the 
    <a href="http://scholar.harvard.edu/files/dtingley/files/topicmodelsopenendedexperiments.pdf">structural
      topic model</a>.  It scales to large corpora and has a graphical
      user interface that anyone can use. With Lucene, txtorg can
      support a wide range of languages. For more information on
      txtorg and text analysis, especially (but not exclusively) with
      data in political science, we point users to a
    <a href="http://scholar.harvard.edu/files/dtingley/files/comparativepoliticstext.pdf">working
      paper</a> that describes the software and various applications
      in greater detail.</p>

  <p>For regular updates and software support, sign up for
    our <a href="https://groups.google.com/forum/#!forum/txtorg-mailing-list">mailing
    list</a>.

    <h1>
      <a name="installation" class="anchor" href="#installation"><span class="octicon octicon-link"></span></a>Installation</h1>

  <p>To use txtorg, you must first install several dependencies. We've
    done our best to simplify and document the installation process
    for
    <a href="installation/linux.html">Linux</a>, <a href="installation/windows.html">Windows</a>, and <a href="installation/mac.html">Mac</a>, but
    we're still improving the installation instructions. If you have any trouble with the installation or if you have ideas for improving it, 
    <a href="mailto:lucas.christopherd@gmail.com">send Chris an email</a>! Your feedback is very helpful.</p>
  
  <h1>
    <a name="how-to" class="anchor"
       href="#how-to"><span class="octicon
				   octicon-link"></span></a>txtorg how-to</h1> This section
  explains how to use txtorg. Check back for frequent updates.
  
  <h3>
    <a name="loading" class="anchor"
       href="#loading"><span class="octicon
				    octicon-link"></span></a>Loading your corpus</h3>
  
  
  <ol>
    
    <li>Create a new corpus. To do so, click File -> New
      Corpus. You'll be prompted to select a place to store the
      corpus.</li>  <br />
    
    <li>The corpus should show up in the corpus window. Now select
      your corpus by clicking on it.</li>  <br />
    
    <li>Next, import some documents. With your corpus highlighted,
      click Corpus -> Import Documents. Next, select the format of
      your corpus. We support several different corpus options
      described below.</li>  <br />

    <li>To import all the documents in a directory (a folder), select
      'Import an entire directory'. These must be .txt files. In this
      case, you do not have any metadata about the documents that you
      are uploading.</li>  <br />

    <li>To import documents from a .csv with a field containing the
      filepaths of all the documents in the corpus, select 'Import
      from a CSV file (not including content)'. Then select the field
      containing the filepaths. brothersk_without_content.csv, in the
      examples directory, is an example of one such csv.</li>  <br />

    <li>To import documents from a .csv with a field containing the
      full documents, select 'Import from a CSV file (including
      content)'. Then select the field containing the
      documents. brothersk_with_content.csv, in the examples
      directory, is an example of one such csv.</li>  <br /> NOTE: If
      you want to import metadata for your documents, you must import
      the documents from a csv containing content. The content field
      is uploaded as the docs, while the remaining fields are uploaded
      as metadata.
  </ol>

  <h3>
    <a name="export" class="anchor" href="#export"><span class="octicon octicon-link"></span></a>Exporting a tdm</h3>
	
  <ol>
    <li>The documents should be imported already. If not, see the previous section.</li>
    <br />
    <li>Now pick your analyzer. Corpus -> Change Analyzer. Just click on the analyzer you want and then click OK. To see the difference between the different analyzers, enter text in the sample window, and select an analyzer. The tokens output by that analzyer will appear in the main window.</li>	
    <br />
    <li>Now rebuild the index file by clicking Corpus -> Rebuild Index File.</li>	
    <br />
    <li>Now select docs. To select all the docs in the corpus, search for 'all'. To subset, use a valid Lucene query.</li>	
    <br />
    <li>To export the tdm for the selected docs, click Export TDM. Then select the format.</li>	
    <br />
    <li>STM format will write a TDM, metadata file, and vocab list. The tdm will be in the format '[M] [term_1]:[count_1] [term_2]:[count_2] ... [term_N]:[count_3]', where [M] is the number of unique terms in the document, [term_i] is an integer associated with the i-th term in the vocabulary, and [count_i] is how many times the i-th term appeared in the document. This is the most common format.</li>	
    <br />
    <li>CTM format will be the same as STM format, except it will be delimited by commas and will include a field for the lucene ID.</li>	
    <br />
    <li>Flat CSV will export a TDM, metadata file, and vocab list. The tdm will be a flat csv, with lots of zeros.</li>
  </ol>
  
</section>
<?php include 'php/footer.php'; ?>
