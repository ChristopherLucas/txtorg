from lucene import *

class AnalyzerUtils(object):
    '''
    Stolen from LuceneInAction.
    '''
    def main(cls, argv):

        print "SimpleAnalyzer"
        cls.displayTokensWithFullDetails(SimpleAnalyzer(),
                                         "The quick brown fox....")

        print "\n----"
        print "StandardAnalyzer"
        cls.displayTokensWithFullDetails(StandardAnalyzer(Version.LUCENE_CURRENT), "I'll e-mail you at xyz@example.com")

    def setPositionIncrement(cls, source, posIncr):
        attr = source.addAttribute(PositionIncrementAttribute.class_)
        attr.setPositionIncrement(posIncr)

    def getPositionIncrement(cls, source):
        attr = source.addAttribute(PositionIncrementAttribute.class_)
        return attr.getPositionIncrement()

    def setTerm(cls, source, term):
        attr = source.addAttribute(TermAttribute.class_)
        attr.setTermBuffer(term)

    def getTerm(cls, source):
        attr = source.addAttribute(TermAttribute.class_)
        return attr.term()

    def setType(cls, source, type):
        attr = source.addAttribute(TypeAttribute.class_)
        attr.setType(type)

    def getType(cls, source):
        attr = source.addAttribute(TypeAttribute.class_)
        return attr.type()

    def displayTokens(cls, analyzer, text):

        tokenStream = analyzer.tokenStream("contents", StringReader(text))
        term = tokenStream.addAttribute(TermAttribute.class_)

        while tokenStream.incrementToken():
            print "[%s]" %(term.term()),

    def displayTokensWithPositions(cls, analyzer, text):

        stream = analyzer.tokenStream("contents", StringReader(text))
        term = stream.addAttribute(TermAttribute.class_)
        posIncr = stream.addAttribute(PositionIncrementAttribute.class_)

        position = 0
        while stream.incrementToken():
            increment = posIncr.getPositionIncrement()
            if increment > 0:
                position = position + increment
                print "\n%d:" %(position),

            print "[%s]" %(term.term()),
        print

    def displayTokensWithFullDetails(cls, analyzer, text):

        stream = analyzer.tokenStream("contents", StringReader(text))

        term = stream.addAttribute(TermAttribute.class_)
        posIncr = stream.addAttribute(PositionIncrementAttribute.class_)
        offset = stream.addAttribute(OffsetAttribute.class_)
        type = stream.addAttribute(TypeAttribute.class_)

        position = 0
        while stream.incrementToken():
            increment = posIncr.getPositionIncrement()
            if increment > 0:
                position = position + increment
                print "\n%d:" %(position),

            print "[%s:%d->%d:%s]" %(term.term(),
                                     offset.startOffset(),
                                     offset.endOffset(),
                                     type.type()),
        print

    def assertAnalyzesTo(cls, analyzer, input, outputs):

        stream = analyzer.tokenStream("field", StringReader(input))
        termAttr = stream.addAttribute(TermAttribute.class_)
        for output in outputs:
            if not stream.incrementToken():
                raise AssertionError, 'stream.incremementToken()'
            if output != termAttr.term():
                raise AssertionError, 'output == termAttr.term())'

        if stream.incrementToken():
            raise AssertionError, 'not stream.incremementToken()'

        stream.close()

    main = classmethod(main)
    setPositionIncrement = classmethod(setPositionIncrement)
    getPositionIncrement = classmethod(getPositionIncrement)
    setTerm = classmethod(setTerm)
    getTerm = classmethod(getTerm)
    setType = classmethod(setType)
    getType = classmethod(getType)
    displayTokens = classmethod(displayTokens)
    displayTokensWithPositions = classmethod(displayTokensWithPositions)
    displayTokensWithFullDetails = classmethod(displayTokensWithFullDetails)
    assertAnalyzesTo = classmethod(assertAnalyzesTo)
