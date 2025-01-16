import unittest
from pyterrier_services import DblpApi

class TestDblp(unittest.TestCase):
    def test_retriever(self):
        dblp = DblpApi()
        retr = dblp.retriever(num_results=10)
        retr.search('PyTerrier')

    def test_bibtex_loader(self):
        dblp = DblpApi()
        loader = dblp.bibtex_loader()
        loader([{'docno': 'conf/cikm/MacdonaldTMO21'}])
