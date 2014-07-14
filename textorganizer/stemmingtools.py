try:
    from lucene import StandardTokenizer, HashSet, Arrays, Version, EnglishPossessiveFilter, LowerCaseFilter
    from lucene import *
except:
    from org.apache.lucene.analysis.standard import *
    from java.util import HashSet, Arrays
    from org.apache.lucene.util import *
    from org.apache.lucene.analysis.en import *
    from org.apache.lucene.analysis.core import *
    from org.apache.lucene.queryparser.classic import *
    from org.apache.pylucene.analysis import *


import codecs
from analyzerutils import AnalyzerUtils
from filters import *
import stops



class PorterStemmerAnalyzerBasic(PythonAnalyzer):
    '''
    An analyzer that stems and removes stopwords.
    '''

    def tokenStream(self, fieldName, reader):
        morestops = HashSet(Arrays.asList(
            stops.contractions+stops.basewords))
        result = StandardTokenizer(Version.LUCENE_CURRENT, reader)
        #result = NumericFilter(result)
        #result = PositionalNumericFilter(result)
        #result = PunctuationFilter(result)
        #result = SNumericFilter(result)
        if VERSION == '2.9.4':
            result = EnglishPossessiveFilterHC(result)
        else:
            result = EnglishPossessiveFilter(result)
        result = StandardFilter(result)
        result = LowerCaseFilter(result)
        #result = StopFilter(True, result, StopAnalyzer.ENGLISH_STOP_WORDS_SET)
        result = StopFilter(True, result, morestops)
        result = PorterStemFilter(result)
	#result = StopFilter(True, result, StopAnalyzer.ENGLISH_STOP_WORDS_SET)
        return result


class PorterStemmerAnalyzerPhrases(PythonAnalyzer):
    '''
    An analyzer that uses the phrase filter and a list of phrases
    to add tokens for phrases as well as applying the porter stemming
    algorithm.
    '''
    def __init__(self, phrase_file = None):
        PythonAnalyzer.__init__(self)
        self.myPhrases = self.get_phrases(phrase_file)

    def get_phrases(self, phrase_file):
        if not phrase_file:
            return None
        try:
            with codecs.open(phrase_file, 'r') as inf:
                return [line.strip() for line in inf]
        except:
            return None

    def tokenStream(self, fieldName, reader):

        result = StandardTokenizer(Version.LUCENE_CURRENT, reader)
        result = StandardFilter(result)
        result = LowerCaseFilter(result)
        result = StopFilter(True, result, StopAnalyzer.ENGLISH_STOP_WORDS_SET)
        result = PorterStemFilter(result)
        if self.myPhrases:
            result = PhraseFilter(result,self.myPhrases)
        return result

class QueryAnalyzer(PythonAnalyzer):
    '''
    An analyzer that uses the same filter chain as the
    PorterStemmerAnalyzer, enabling analysis  of the individual phrases
    using the Porter stemming algorithm and standard tokenizer.
    '''

    def tokenStream(self, fieldName, reader):

        result = StandardTokenizer(Version.LUCENE_CURRENT, reader)
        result = StandardFilter(result)
        result = LowerCaseFilter(result)
        result = PorterStemFilter(result)
        return result

def stemPhrases(allPhrases,analyzer):
    '''
    We need to porter stem the phrases in the query so that it will
    match the porterized versions.  Added benefit: if you are looking
    for the exact phrase 'buffalo wing'  you will also get 'buffalo wings'
    bug or feature?  you decide!

    sample call: stemPhrases(allPhrases,QueryAnalyzer)
    '''

    stemmedPhrases = []

    for p in allPhrases:
        query = QueryParser(Version.LUCENE_CURRENT, "removeme",
                            analyzer(Version.LUCENE_CURRENT)).parse('"'+p+'"')
        stemmedQuery = query.toString()
        stemmedPhrase = stemmedQuery.replace('removeme:','').replace('"','')
        stemmedPhrases.append(stemmedPhrase)

    return stemmedPhrases


def init_PSA(phrasefile):

    print "Reading phrase definitions from %s..." % (phrasefile,)
    all_phrases = []
    try:
        with codecs.open(phrasefile,'r',encoding='UTF-8') as inf:
            for line in inf:
                all_phrases.append(line.strip())
    except:
        print "Failed. Disabling PhraseFilter"

    stemmedPhrases = stemPhrases(all_phrases,QueryAnalyzer)

    psa = PorterStemmerAnalyzer(Version.LUCENE_CURRENT)
    psa.setPhrases(stemmedPhrases)
    return psa


if __name__ == '__main__':
    print stemPhrases(['test phrase','another test'],QueryAnalyzer)
