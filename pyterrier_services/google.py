from typing import Optional, Union, Tuple
import os
import pandas as pd
import pyterrier as pt
from pyterrier_services import paginated_search, multi_query

_HELP_URL = 'https://developers.google.com/custom-search/v1/overview'

class GoogleApi:
    """Represents a refernece to the Google API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Args: 
            api_key (str): the Google API key (taken from ``GOOGLE_API_KEY`` env variable if not provided)
        """
        if api_key is None:
            api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key is None:
            raise ValueError(f"A Google API key must be specified (either as GOOGLE_API_KEY env variable or passed to `GoogleApi(api_key='...')`). See <{_HELP_URL}> for details on how to get an API key.")
        self.api_key = api_key

        try:
            from googleapiclient.discovery import build
        except ModuleNotFoundError as mnfe:
            raise Exception("You need to pip install google-api-python-client") from mnfe
        self._build = build

    def retriever(self, cx: Optional[str] = None, *, num_results: int = 10, verbose: bool = False) -> pt.Transformer:
        """Creates a :class:`GoogleSearchRetriever` instance, allowing retrieval over the Google search engine.

        Follow Google's guide for a `Custom Search JSON API <{_HELP_URL}>`_ to get
        the right parameters.

        Arguments:
            cx (str): the service to access (taken from ``GOOGLE_CSE_CX`` env variable if not provided)
            num_results (int): The number of results to retrieve per query. Defaults to 10.

        Returns:
            :class:`pyterrier.Transformer`: A PyTerrier transformer that can be used to
            perform Google searches.

        Output columns: ['title', 'url', 'snippet']

        Example::
            title               Chemical reaction | Definition, Equations, Exa...
            url                 https://www.britannica.com/science/chemical-re...
            snippet             Mar 24, 2025 ... A chemical reaction is a proc...
        """.format(_HELP_URL=_HELP_URL)
        return GoogleSearchRetriever(self, cx, num_results=num_results, verbose=verbose)


class GoogleSearchRetriever(pt.Transformer):
    """A :class:`~pyterrier.Transformer` retriever that queries the Google search API."""

    def __init__(self,
        api: Optional[GoogleApi] = None,
        cx: Optional[str] = None,
        *,
        num_results: int = 10,
        verbose: bool = False,
    ):
        """
        Args:
            api (GoogleApi): The Google API service. Defaults to a new instance of :class:`GoogleApi`.
            cx: (str): The Google Custom Search Engine ID. This is required to perform searches.
            num_results (int): The number of results to retrieve per query. Defaults to 10.
            verbose (bool): Whether to log the progress. Defaults to False.
        """
        self.api = api or GoogleApi()
        if cx is None:
            cx = os.getenv("GOOGLE_CSE_CX")
        if cx is None:
            raise ValueError(f"A Google Custom Search Engine ID (cx) must be specified. See <{_HELP_URL}> for details on how to get a Custom Search Engine ID.")
        self.cx = cx
        self.cse_service = self.api._build("customsearch", "v1", developerKey=self.api.api_key).cse()
        self.num_results = num_results
        self.verbose = verbose

    def transform(self, inp: pd.DataFrame) -> pd.DataFrame:
        return multi_query(
            paginated_search(self._search_internal, num_results=self.num_results),
            verbose=self.verbose,
            verbose_desc='GoogleSearchRetriever',
        )(inp)

    def _search_internal(self,
        query: str,
        *,
        offset: int = 0,
        limit: int = 10,
        return_next: bool = False,
        return_total: bool = False
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame, int], Tuple[pd.DataFrame, int, int]]:
        """Searches for papers on Google with the provided query.

        Args:
            query: The search query.
            offset: The offset of the first result to retrieve. Defaults to 0.
            limit: The maximum number of results to retrieve. Defaults to 10.
            return_next: Whether to return the next query URL. Defaults to False.
            return_total: Whether to return the total number of results. Defaults to False.
        """
        api_result = self.cse_service.list(q=query, cx=self.cx, num=min(limit, 10), start=offset).execute()
        if len(api_result["items"]) == 0:
            result_df = pd.DataFrame(columns=['docno', 'url', 'title', 'snippet', 'rank', 'score'])
        else:
            result_df = pd.DataFrame([[r['link'], r['link'], r['title'], r['snippet']] for r in api_result["items"]], columns=['docno', 'url', 'title', 'snippet'])
            result_df['rank'] = range(offset, offset+len(result_df))
            result_df['score'] = -result_df['rank']

        res = [result_df]
        if return_next:
            res.append(offset + len(result_df) + 1)
        if return_total:
            res.append(int(res['searchInformation']['totalResults']))
        if len(res) == 1:
            return res[0]
        return tuple(res)

    def fuse_rank_cutoff(self, k: int) -> Optional['GoogleSearchRetriever']:
        if k < self.num_results:
            return GoogleSearchRetriever(api=self.api, cx=self.cx, num_results=k, verbose=self.verbose)
