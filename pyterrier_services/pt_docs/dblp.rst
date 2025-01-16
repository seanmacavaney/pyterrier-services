DBLP
==================================================

`DBLP <https://dblp.org/>`__ provides open bibliographic information on computer science journals and conferences.

``pyterrier-services`` provides access to DBLP APIs through :class:`~pyterrier_services.DblpApi`.

Example:

.. code-block:: python
    :caption: Retrieve from the DBLP API

    >>> from pyterrier_services import DblpApi
    >>> dblp = DblpApi()
    >>> retr = dblp.retriever(num_results=5)
    >>> dblp.search('pyterrier')
    #   qid      query                         docno  score  rank                                              title                                            authors  year                             type
    # 0   1  pyterrier  journals/corr/abs-2412-05339   -0.0     0  PyTerrier-GenRank: The PyTerrier Plugin for Re...                                [Kaustubh D. Dhole]  2024  Informal and Other Publications
    # 1   1  pyterrier      conf/cikm/MacdonaldTMO21   -1.0     1  PyTerrier: Declarative Experimentation in Pyth...  [Craig Macdonald, Nicola Tonellotto, Sean MacA...  2021   Conference and Workshop Papers
    # 2   1  pyterrier  conf/clef/Tavakolpoursaleh21   -2.0     2  PyTerrier-based Research Data Recommendations ...         [Narges Tavakolpoursaleh, Johann Schaible]  2021   Conference and Workshop Papers
    # 3   1  pyterrier       conf/ictir/MacdonaldT20   -3.0     3  Declarative Experimentation in Information Ret...               [Craig Macdonald, Nicola Tonellotto]  2020   Conference and Workshop Papers
    # 4   1  pyterrier  journals/corr/abs-2007-14271   -4.0     4  Declarative Experimentation in Information Ret...               [Craig Macdonald, Nicola Tonellotto]  2020  Informal and Other Publications


.. autoclass:: pyterrier_services.DblpApi
   :members:

.. autoclass:: pyterrier_services.DblpRetriever
   :members:

.. autoclass:: pyterrier_services.DblpBibtexLoader
   :members:
