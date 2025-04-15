Google API
==================================================


``pyterrier-services`` provides access to the Google Search API through
:class:`~pyterrier_services.GoogleApi`.

You need to set up a Google API key and a custom search engine (CSE) ID.
See https://developers.google.com/custom-search/v1/overview for more information.

You can either set your API key and CSE ID as environment variables
``GOOGLE_API_KEY`` and ``GOOGLE_CSE_ID`` or pass them as arguments to
:class:`~pyterrier_services.GoogleApi` and :class:`~pyterrier_services.GoogleSearchRetriever`.

.. note::
	
	One request will be made to the Google API for every 10 results for every query.
	This can quickly add up to a lot of requests, so be careful with the number of queries
	issued and the ``num_results`` parameter (which defaults to 10 to issue a single request per query).

Example:

.. code-block:: python
	:caption: Retrieve from the Google API

	>>> from pyterrier_services import GoogleApi
	>>> google = GoogleApi(api_key=...) # or provide via GOOGLE_API_KEY
	>>> retr = google.retriever(cs=..., num_results=15) # or provide via GOOGLE_CSE_ID
	>>> retr.search('pyterrier')
	   qid      query                                              docno  score  rank                                                url                                              title                                            snippet
	0    1  pyterrier           https://github.com/terrier-org/pyterrier      0     0           https://github.com/terrier-org/pyterrier  terrier-org/pyterrier: A Python framework for ...  PyTerrier provides an Experiment function, whi...
	1    1  pyterrier                  https://pyterrier.readthedocs.io/     -1     1                  https://pyterrier.readthedocs.io/                                   PyTerrier 0.13.0  Guides. Installing and Configuring · Importing...
	2    1  pyterrier  https://cs.usm.maine.edu/~behrooz.mansouri/cou...     -2     2  https://cs.usm.maine.edu/~behrooz.mansouri/cou...  Introduction to Information Retrieval -- Sessi...  ... pyterrier.git. ○ All usages of PyTerrier s...
	3    1  pyterrier  https://pyterrier.readthedocs.io/en/latest/par...     -3     3  https://pyterrier.readthedocs.io/en/latest/par...                 Parallelisation - PyTerrier 0.13.0  Parallelisation occurs by partitioning datafra...
	4    1  pyterrier     https://dl.acm.org/doi/10.1145/3459637.3482013     -4     4     https://dl.acm.org/doi/10.1145/3459637.3482013  PyTerrier: Declarative Experimentation in Pyth...  Abstract. PyTerrier is a Python-based retrieva...
	5    1  pyterrier  https://colab.research.google.com/github/terri...     -5     5  https://colab.research.google.com/github/terri...                            PyTerrier Indexing Demo  This notebook takes you through indexing using...
	6    1  pyterrier                   https://arxiv.org/abs/2007.14271     -6     6                   https://arxiv.org/abs/2007.14271  Declarative Experimentation in Information Ret...  Jul 28, 2020 ... A framework called PyTerrier ...
	7    1  pyterrier             https://ir-datasets.com/pyterrier.html     -7     7             https://ir-datasets.com/pyterrier.html                            PyTerrier & ir_datasets  Indexing a Dataset. The pt.IterDictIndexer cla...
	8    1  pyterrier           https://pypi.org/project/python-terrier/     -8     8           https://pypi.org/project/python-terrier/                              python-terrier · PyPI  Pyjnius/PyTerrier will pick up the location au...
	9    1  pyterrier  https://in-d-docs-demo.readthedocs.io/en/lates...     -9     9  https://in-d-docs-demo.readthedocs.io/en/lates...  Installing and Configuring — PyTerrier 0.8.1 d...  If you wish to run PyTerrier in an offline env...
	10   1  pyterrier      https://eprints.gla.ac.uk/249268/2/249268.pdf    -11    11      https://eprints.gla.ac.uk/249268/2/249268.pdf  PyTerrier: Declarative Experimentation in Pyth...  Nov 3, 2021 ... ABSTRACT. PyTerrier is a Pytho...
	11   1  pyterrier  https://ui.adsabs.harvard.edu/abs/2020arXiv200...    -12    12  https://ui.adsabs.harvard.edu/abs/2020arXiv200...  Declarative Experimentation in Information Ret...  ... PyTerrier that allows advanced retrieval p...
	12   1  pyterrier                              https://ir-measur.es/    -13    13                              https://ir-measur.es/                          ir-measures documentation  See the tabs below for examples using the Comm...
	13   1  pyterrier  https://medium.com/@mkalmus/building-an-inform...    -14    14  https://medium.com/@mkalmus/building-an-inform...  Building An Information Retrieval System for T...  Dec 14, 2021 ... TLDR: We created a system to ...
	14   1  pyterrier         https://ceur-ws.org/Vol-2936/paper-145.pdf    -15    15         https://ceur-ws.org/Vol-2936/paper-145.pdf  PyTerrier-based Research Data Recommendations ...  Pyterrier provides easy to conduct IR experime...



.. autoclass:: pyterrier_services.GoogleApi

.. autoclass:: pyterrier_services.GoogleSearchRetriever
