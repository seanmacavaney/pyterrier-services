Google API
==================================================


``pyterrier-services`` provides access to the Google Search API through
:class:`~pyterrier_services.GoogleApi`.

Example:

.. code-block:: python
	:caption: Retrieve from the Google API

	>>> from pyterrier_services import GoogleApi
	>>> api = GoogleApi(key=...)
	>>> retr = api.retriever(cx=...)
	>>> retr.search('pyterrier')
	# qid      query                                     docno  score  rank                                              title                                           abstract
	#   1  pyterrier  7fa92ed08eee68a945884b8744e7db9887aed9d3      0     0  PyTerrier: Declarative Experimentation in Pyth...  PyTerrier is a Python-based retrieval framewor...
	#   1  pyterrier  a6b1126e058262c57d36012d0fdedc2417ad04e1     -1     1  Declarative Experimentation in Information Ret...  The advent of deep machine learning platforms ...
	#   1  pyterrier  833b453c621099bccca028752aaa74262123706a     -2     2  PyTerrier-based Research Data Recommendations ...  Research data is of high importance in scienti...
	#   1  pyterrier  73feb5cfe491342d52d47e8817d113c072067306     -3     3      The Information Retrieval Experiment Platform  We integrate irdatasets, ir_measures, and PyTe...
	#   1  pyterrier  90b8a1adae2761e48c87fdeb68a595dc11161970     -4     4  QPPTK@TIREx: Simplified Query Performance Pred...  We describe our software submission to the ECI...


.. autoclass:: pyterrier_services.GoogleApi
