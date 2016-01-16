import whoosh
from whoosh.compat import u, text_type
from whoosh.analysis import StandardAnalyzer, SimpleAnalyzer, StopFilter, Tokenizer
from whoosh.searching import Searcher
from whoosh.index import exists_in, create_in, open_dir
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.analysis.acore import Composable, Token

import lucene
from java.io import StringReader
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute

import lucene
import os

#You can compose tokenizers and filters together using the | character:
# my_analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter()

class LuceneTokenizer(Tokenizer):
    """An Lucene tokenizer based on Nielsen's Stemmer
    """

    def __init__(self, luceneanalyzer):
        """
        :param expression: A regular expression object or string. Each match
            of the expression equals a token. Group 0 (the entire matched text)
            is used as the text of the token. If you require more complicated
            handling of the expression match, simply write your own tokenizer.
        :param gaps: If True, the tokenizer *splits* on the expression, rather
            than matching on the expression.
        """
        lucene.initVM()
        # luceneananalyzer is an analyzer, e.g., StandardAnalyzer
        # from org.apache.lucene.analysis.standard import StandardAnalyzer
        self.lanalyzer = luceneanalyzer()
        
    
    def __call__(self, value, positions=False, chars=False, keeporiginal=False,
                 removestops=True, start_pos=0, start_char=0, tokenize=True,
                  mode='', **kwargs):
        """
        :param value: The unicode string to tokenize.
        :param positions: Whether to record token positions in the token.
        :param chars: Whether to record character offsets in the token.
        :param start_pos: The position number of the first token. For example,
            if you set start_pos=2, the tokens will be numbered 2,3,4,...
            instead of 0,1,2,...
        :param start_char: The offset of the first character of the first
            token. For example, if you set start_char=2, the text "aaa bbb"
            will have chars (2,5),(6,9) instead (0,3),(4,7).
        :param tokenize: if True, the text should be tokenized.
        """
        assert isinstance(value, text_type), "%r is not unicode" % value

        tokenlist = []
        tokenStream = self.lanalyzer.tokenStream("contents", StringReader(value))
        #term = tokenStream.addAttribute(lucene.TermAttribute.class_)
        tokenStream.reset()
        
        if len(value)>0:
            while tokenStream.incrementToken():
                tokenlist.append(tokenStream.getAttribute(CharTermAttribute.class_).toString())
                #self.tokentext.insert(END, "[%s]" %(term.term()))
        

        t = Token(positions, chars, removestops=removestops, mode=mode,
                  **kwargs)
        if not tokenize:
            t.original = t.text = value
            t.boost = 1.0
            if positions:
                t.pos = start_pos
            if chars:
                t.startchar = start_char
                t.endchar = start_char + len(value)
            yield t
        else:
            for (pos,text) in enumerate(tokenlist):
                # we may have some off by one errors
                # what is the starting character of the token?
                #start_char_t = value[start_char:].find(text)+start_char
                t.text = text
                #print pos, start_char_t, text
                if positions:
                    print "Unsupported!"
                    #t.pos = start_pos+pos
                    t.pos = pos
                if chars:
                    print "Unsupported!"                    
                    t.startchar = pos
                    t.endchar = pos
                yield t
                # make the tokens
                # copying from https://bitbucket.org/mchaput/whoosh/src/c9ad870378a0f5167182349b64fc3e09c6ca12df/src/whoosh/analysis/tokenizers.py?at=default


#def LuceneAnalyzer():    
#    return LuceneTokenizer(luceneanalyzer)
