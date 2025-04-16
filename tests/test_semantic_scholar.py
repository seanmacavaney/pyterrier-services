import unittest
import pandas as pd
from pyterrier_services import SemanticScholarApi

class TestSemanticScholar(unittest.TestCase):
    def test_retriever(self):
        s2 = SemanticScholarApi()
        retr = s2.retriever(num_results=15)
        res = retr.search('pyterrier')
        self.assertIsInstance(res, pd.DataFrame)
        self.assertEqual(len(res), 15)
        self.assertEqual(set(res.columns), {'qid', 'query', 'docno', 'score', 'rank', 'title', 'abstract', 'authors', 'openAccessPdf'})
