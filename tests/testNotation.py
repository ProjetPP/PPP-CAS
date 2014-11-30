from ppp_cas.notation import isMath, traceContainsSpellChecker
from unittest import TestCase
from ppp_datamodel import Sentence, Resource
from ppp_datamodel.communication import TraceItem

class TestSympy(TestCase):

    def testIsMath(self):
        mathematicalExpressions=['Sin[x]',
                                 'sin(x)',
                                 'Arctan[x]',
                                 'atan(x)',
                                 'x**2',
                                 'x^2',
                                 '(a)*b',
                                 '(a)b',
                                 'a/=b',
                                 '\\frac{\pi^{2}}{6}',
                                 'integrate(exp(-x**2/2), (x,(-oo,oo)))',
                                 'diff(x**2,x)',
                                 '(a/(b+1)/c)+1/(d+1)',
                                 'sqrt(2)'
                                ]
        naturalLanguageSentences=['What is the birth date of the president of the United States?',
                                  'What is the birth date of George Washington?',
                                  'Who is the director of \"Pulp Fiction\"?',
                                  'Who is the president of France?',
                                  'What is the capital of Australia?',
                                  'Who is the author of \"Foundation\"?'
                                 ]
        for e in mathematicalExpressions:
            self.assertTrue(isMath(e))
        for e in naturalLanguageSentences:
            self.assertFalse(isMath(e))
            
    def testTraceContainsSpellChecker(self):
        tracesWithoutSpellChecker=[[TraceItem('CAS', Resource('42', value_type='math-latex'), {'accuracy': 0, 'relevance': 0})],
                                   [TraceItem('CAS', Resource('42', value_type='math-latex'), {'accuracy': 0, 'relevance': 0}), TraceItem('input', Sentence('sqrt(2)'), {'accuracy': 0, 'relevance': 0})],
                                   [TraceItem('input', Sentence('sqrt(2)'), {'accuracy': 0, 'relevance': 0}), TraceItem('CAS', Resource('42', value_type='math-latex'), {'accuracy': 0, 'relevance': 0})],
                                  ]
        tracesWithSpellChecker=[[TraceItem('spell-checker', Sentence('sqrt(2)'),  {'accuracy': 0, 'relevance': 0})],
                                [TraceItem('input', Sentence('sqrt(2)'), {'accuracy': 0, 'relevance': 0}), TraceItem('spell-checker', Sentence('sq rt 2'), {'accuracy': 0, 'relevance': 0})],
                                [TraceItem('spell-checker', Sentence('sq rt 2'), {'accuracy': 0, 'relevance': 0}), TraceItem('input', Sentence('sqrt(2)'), {'accuracy': 0, 'relevance': 0})],
                               ]
        
        for e in tracesWithSpellChecker:
            self.assertTrue(traceContainsSpellChecker(e))
        for e in tracesWithoutSpellChecker:
            self.assertFalse(traceContainsSpellChecker(e))
        
