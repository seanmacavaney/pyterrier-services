from typing import Optional, Union, Tuple
from functools import partial
from enum import Enum
import pandas as pd
import requests
import pyterrier as pt
import pyterrier_alpha as pta
from . import http_error_retry, paginated_search, multi_query


class DblpEntityType(Enum):
    publication = 'publication'
    author = 'author'
    venue = 'venue'


class DblpBibType(Enum):
    standard = 'standard'
    condensed = 'condensed'
    with_crossref = 'with_crossref'


class DblpApi:
    """Represents a reference to the DBLP search API."""

    API_BASE_URL = 'https://dblp.org'

    def retriever(self,
        *,
        num_results: int = 100,
        entity_type: Union[str, DblpEntityType] = DblpEntityType.publication,
        verbose: bool = True
    ) -> pt.Transformer:
        """Returns a :class:`~pyterrier.Transformer` that retrieves from DBLP.

        Args:
            num_results: The number of results to retrieve. Defaults to 100.
            entity_type: The type of entity to search over. Defaults to ``DblpEntityType.publication``.
            verbose: Whether to log the progress. Defaults to True.
        """
        return DblpRetriever(api=self, num_results=num_results, entity_type=entity_type, verbose=verbose)

    def bibtex_loader(self,
        *,
        bib_type: Union[str, DblpBibType] = DblpBibType.standard,
        verbose: bool = True
    ) -> pt.Transformer:
        """Returns a :class:`~pyterrier.Transformer` that loads bibtex data from DBLP.

        Args:
            bib_type: The type of BibTeX to load. Defaults to ``DblpBibType.standard``.
            verbose: Whether to log the progress. Defaults to True.
        """
        return DblpBibtexLoader(api=self, bib_type=bib_type, verbose=verbose)

    def search(self,
        query: str,
        *,
        entity_type: Union[str, DblpEntityType] = DblpEntityType.publication,
        offset: int = 0,
        limit: int = 100,
        return_next: bool = False,
        return_total: bool = False,
    ) -> Union[pd.DataFrame, Tuple[pd.DataFrame, int], Tuple[pd.DataFrame, int, int]]:
        """Searches for papers on Semantic Scholar with the provided query.

        Args:
            query: The search query.
            entity_type: The type of entity to search over. Defaults to ``DblpEntityType.publication``.
            offset: The offset of the first result to retrieve. Defaults to 0.
            limit: The maximum number of results to retrieve. Defaults to 100.
            return_next: Whether to return the next query URL. Defaults to False.
            return_total: Whether to return the total number of results. Defaults to False.
        """
        entity_type = DblpEntityType(entity_type)
        limit = max(min(limit, 1000), 1)
        params = {
            'q': query,
            'format': 'json',
            'f': offset,
            'c': limit,
        }
        endpoint = {
            DblpEntityType.publication: '/search/publ/api',
            DblpEntityType.author: '/search/author/api',
            DblpEntityType.venue: '/search/venue/api',
        }[entity_type]
        http_res = requests.get(DblpApi.API_BASE_URL + endpoint, params=params)
        http_res.raise_for_status()
        http_res = http_res.json()['result']

        data_columns, docno_column = {
            DblpEntityType.publication: (['title', 'authors', 'year', 'type'], 'key'),
            DblpEntityType.author: (['author'], '@id'),
            DblpEntityType.venue: (['venue', 'acronym', 'type'], '@id'),
        }[entity_type]

        result_df = []
        first = int(http_res['hits']['@first'])
        for rank, hit in zip(range(limit), http_res['hits'].get('hit', [])):
            row = [
                hit['info'][docno_column] if docno_column != '@id' else hit['@id'],
                first + rank,
                -1.0 * (first + rank),
            ]
            for c in data_columns:
                if c == 'authors':
                    authors = hit['info'][c]['author']
                    if isinstance(authors, dict):
                        authors = [authors]
                    row.append([a['text'] for a in authors])
                else:
                    row.append(hit['info'][c])
            result_df.append(row)
        result_df = pd.DataFrame(result_df, columns=['docno', 'rank', 'score', *data_columns])

        res = [result_df]
        if return_next:
            res.append(first + int(http_res['hits']['@sent']))
        if return_total:
            res.append(int(http_res['hits']['@total']))
        if len(res) == 1:
            return res[0]
        return tuple(res)

    def load_bibtex(self,
        docno: str,
        *,
        bib_type: Union[str, DblpBibType] = DblpBibType.standard,
    ) -> str:
        bib_type = DblpBibType(bib_type)
        param = {
            DblpBibType.standard: '1',
            DblpBibType.condensed: '0',
            DblpBibType.with_crossref: '2',
        }[bib_type]
        http_res = requests.get(f'{DblpApi.API_BASE_URL}/rec/{docno}.bib', params={'param': param})
        http_res.raise_for_status()
        return http_res.text


class DblpRetriever(pt.Transformer):
    """A :class:`~pyterrier.Transformer` retriever that queries the DBLP search API."""
    def __init__(self,
        *,
        api: Optional[DblpApi] = None,
        num_results: int = 100,
        entity_type: Union[str, DblpEntityType] = DblpEntityType.publication,
        verbose: bool = True
    ):
        """
        Args:
            api: The DBLP api service. Defaults to a new instance of :class:`~pyterrier_services.DblpApi`.
            num_results: The number of results to retrieve per query. Defaults to 100.
            entity_type: The type of entity to search over. Defaults to ``DblpEntityType.publication``
            verbose: Whether to log the progress. Defaults to True.
        """
        self.api = api or DblpApi()
        self.num_results = num_results
        self.entity_type = entity_type
        self.verbose = verbose

    def transform(self, inp: pd.DataFrame) -> pd.DataFrame:
        pta.validate.query_frame(inp, extra_columns=['query'])
        return multi_query(
            paginated_search(
                http_error_retry(
                    partial(self.api.search, entity_type=self.entity_type)
                ),
                num_results=self.num_results,
            ),
            verbose=self.verbose,
            verbose_desc='DblpRetriever',
        )(inp)

    def fuse_rank_cutoff(self, k: int) -> Optional['DblpRetriever']:
        if k < self.num_results:
            return DblpRetriever(api=self.api, num_results=k, entity_type=self.entity_type, verbose=self.verbose)


class DblpBibtexLoader(pt.Transformer):
    """A :class:`~pyterrier.Transformer` that loads BibTeX data from DBLP."""
    def __init__(self,
        *,
        api: Optional[DblpApi] = None,
        bib_type: Union[str, DblpBibType] = DblpBibType.standard,
        verbose: bool = True
    ):
        """
        Args:
            api: The DBLP api service. Defaults to a new instance of :class:`~pyterrier_services.DblpApi`.
            bib_type: The type of BibTeX to load. Defaults to ``DblpBibType.standard``.
            verbose: Whether to log the progress. Defaults to True.
        """
        self.api = api or DblpApi()
        self.bib_type = bib_type
        self.verbose = verbose

    def transform(self, inp: pd.DataFrame) -> pd.DataFrame:
        pta.validate.columns(inp, includes=['docno'])
        bibtex = []
        it = inp['docno']
        if self.verbose:
            it = pt.tqdm(it, desc='DblpBibtexLoader')
        for docno in it:
            bibtex.append(self.api.load_bibtex(docno, bib_type=self.bib_type))
        return inp.assign(bibtex=bibtex)
