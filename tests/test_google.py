import unittest
import pandas as pd
from pyterrier_services import GoogleApi

class TestGoogle(unittest.TestCase):
    def test_retriever(self):
        google = GoogleApi()
        retr = google.retriever(num_results=15)
        res = retr.search('PyTerrier')
        self.assertIsInstance(res, pd.DataFrame)
        self.assertEqual(len(res), 15)
        self.assertEqual(set(res.columns), {'qid', 'query', 'docno', 'score', 'rank', 'url', 'title', 'snippet'})
