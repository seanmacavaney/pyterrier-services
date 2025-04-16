import os
import unittest
import pandas as pd
from pyterrier_services import SemanticScholarApi

class TestSemanticScholar(unittest.TestCase):
    @unittest.skipIf('S2_API_KEY' not in os.environ, 'S2_API_KEY not set')
    def test_retriever(self):
        s2 = SemanticScholarApi()
        retr = s2.retriever(num_results=15)
        res = retr.search('test')
        self.assertIsInstance(res, pd.DataFrame)
        self.assertEqual(len(res), 15)
        self.assertEqual(set(res.columns), {'qid', 'query', 'docno', 'score', 'rank', 'url', 'title', 'snippet'})
