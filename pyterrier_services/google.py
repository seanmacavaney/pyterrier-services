
import pyterrier as pt
import pandas as pd

def GoogleSearchRetriever(cx, key) -> pt.Transformer:
    """
    Get a Google Search service object. 
    Follow Google's guide for a `Custom Search JSON API <https://developers.google.com/custom-search/v1/overview>`_ to get
    the right parameters

    Instructions:

    Arguments:
        cx(str) - the service to access
        key(str) - the Google API key

    Returns:
        pt.Transformer: A PyTerrier transformer that can be used to
        perform Google searches.

    Output columns: ['kind', 'title', 'htmlTitle', 'link', 'displayLink', 'snippet',
       'htmlSnippet', 'formattedUrl', 'htmlFormattedUrl', 'pagemap']

    Example::
        kind                                              customsearch#result
        title               Chemical reaction | Definition, Equations, Exa...
        htmlTitle           <b>Chemical reaction</b> | Definition, Equatio...
        link                https://www.britannica.com/science/chemical-re...
        displayLink                                        www.britannica.com
        snippet             Mar 24, 2025 ... A chemical reaction is a proc...
        htmlSnippet         Mar 24, 2025 <b>...</b> A <b>chemical reaction...
        formattedUrl        https://www.britannica.com/science/chemical-re...
        htmlFormattedUrl    https://www.britannica.com/science/<b>chemical...
        pagemap             {'cse_thumbnail': [{'src': 'https://encrypted-...
    """
    try:
        from googleapiclient.discovery import build
    except ModuleNotFoundError as mnfe:
        raise Exception("You need to pip install google-api-python-client") from mnfe

    service = build(
        "customsearch", "v1", developerKey=key
    )
    def _search_google(one_query : pt.model.IterDict) -> pt.model.IterDict:
        res = service.cse().list(q=next(one_query)["query"], cx=cx).execute()
        return res["items"]

    return pt.apply.by_query(_search_google, iter=True)