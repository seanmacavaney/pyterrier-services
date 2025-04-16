import pandas as pd
import unittest
from pyterrier_services import DblpApi

class TestDblp(unittest.TestCase):
    def test_retriever(self):
        dblp = DblpApi()
        retr = dblp.retriever(num_results=5)
        res = retr.search('PyTerrier')
        self.assertIsInstance(res, pd.DataFrame)
        self.assertEqual(len(res), 5)
        self.assertEqual(set(res.columns), {'qid', 'query', 'docno', 'score', 'rank', 'title', 'type', 'authors', 'year'})

    def test_bibtex_loader(self):
        dblp = DblpApi()
        loader = dblp.bibtex_loader()
        res = loader(pd.DataFrame([{'docno': 'conf/cikm/MacdonaldTMO21'}]))
        self.assertIsInstance(res, pd.DataFrame)
        self.assertEqual(len(res), 1)
        self.assertEqual(set(res.columns), {'docno', 'bibtex'})
