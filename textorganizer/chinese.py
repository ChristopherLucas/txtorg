import whoosh
from whoosh.analysis import StandardAnalyzer, SimpleAnalyzer
from whoosh.searching import Searcher
from whoosh.index import exists_in, create_in, open_dir
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT


from snownlp import SnowNLP
from snownlp.normal import *

#You can compose tokenizers and filters together using the | character:
# my_analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter()


class ChineseTokenizer(Tokenizer):
    """A Chinese tokenizer based on SnowNLP:
       https://github.com/isnowfy/snownlp
    """

    def findPos(start_pos,text,value):
        
    
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

        # Thanks, isnowfy!
        s = SnowNLP(value)
        tokenlist = s.words

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
                start_char = value[start_char:].find(text)+start_char
                print pos, start_char, text
                # make the tokens
                # copying from https://bitbucket.org/mchaput/whoosh/src/c9ad870378a0f5167182349b64fc3e09c6ca12df/src/whoosh/analysis/tokenizers.py?at=default
