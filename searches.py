"""Contains core search functionality"""
from typing import List
import os
import requests

MAL = 'mal'
MD = 'md'
MU = 'mu'
NU = 'nu'
SCP = 'scp'
WIKI = 'wiki'
XKCD = 'xkcd'

GOOGLE_SEARCH_API_KEY = os.environ['GOOGLE_SEARCH_API_KEY']

GOOGLE_SEARCH_ENGINE_IDS = {
    MAL: os.environ['GOOGLE_SEARCH_ENGINE_ID_MAL'],
    MD: os.environ['GOOGLE_SEARCH_ENGINE_ID_MD'],
    MU: os.environ['GOOGLE_SEARCH_ENGINE_ID_MU'],
    MU: os.environ['GOOGLE_SEARCH_ENGINE_ID_NU'],
    SCP: os.environ['GOOGLE_SEARCH_ENGINE_ID_SCP'],
    WIKI: os.environ['GOOGLE_SEARCH_ENGINE_ID_WIKI'],
    XKCD: os.environ['GOOGLE_SEARCH_ENGINE_ID_XKCD'],
}

def google_search(search_query: str, num_results: int, search_type: str) -> List[str]:
    """
    Return a list of search results by Google's search engine.

    List elements will be dictionaries with keys as below in the 'items' section:
    https://developers.google.com/custom-search/v1/cse/list#response
    """
    res = requests.get("https://www.googleapis.com/customsearch/v1",
                       params={'key': GOOGLE_SEARCH_API_KEY,
                               'q': search_query,
                               'num': num_results,
                               'cx': GOOGLE_SEARCH_ENGINE_IDS[search_type],
                              }).json()

    # there is no 'items' key if there's an error or no results
    if 'error' in res or not int(res['searchInformation']['totalResults']):
        return []

    return res['items']
