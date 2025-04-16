import os
import unittest
import pandas as pd
from pyterrier_services import PineconeApi

class TestPinecone(unittest.TestCase):
    @unittest.skipIf('PINECONE_API_KEY' not in os.environ, 'PINECONE_API_KEY not set')
    def test_dense(self):
        pinecone = PineconeApi()
        model = pinecone.dense_model()
        res = model.search('PyTerrier')
        self.assertIsInstance(res, pd.DataFrame)
        self.assertEqual(len(res), 1)
        self.assertEqual(set(res.columns), {'qid', 'query', 'query_vec'})

    @unittest.skipIf('PINECONE_API_KEY' not in os.environ, 'PINECONE_API_KEY not set')
    def test_sparse(self):
        pinecone = PineconeApi()
        model = pinecone.sparse_model()
        res = model.search('PyTerrier')
        self.assertIsInstance(res, pd.DataFrame)
        self.assertEqual(len(res), 1)
        self.assertEqual(set(res.columns), {'qid', 'query', 'query_toks'})

    @unittest.skipIf('PINECONE_API_KEY' not in os.environ, 'PINECONE_API_KEY not set')
    def test_reranker(self):
        pinecone = PineconeApi()
        model = pinecone.reranker()
        res = model(pd.DataFrame([
            {'qid': '1', 'query': 'PyTerrier', 'docno': '1', 'text': 'PyTerrier is awesome!'},
            {'qid': '1', 'query': 'PyTerrier', 'docno': '2', 'text': 'Something else'},
        ]))
        self.assertIsInstance(res, pd.DataFrame)
        self.assertEqual(len(res), 2)
        self.assertEqual(set(res.columns), {'qid', 'query', 'docno', 'text', 'rank', 'score'})
