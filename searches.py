from log import logger
from typing import List
import discord
import os
import requests

NO_RESULTS_FOUND_MESSAGE = "No results found"


MAL = 'mal'
MD = 'md'
MU = 'mu'
NU = 'nu'
SCP = 'scp'
STEAM = 'steam'
WIKI = 'wiki'
XKCD = 'xkcd'

ALL_SITES = [MAL, MD, MU, NU, SCP, STEAM, WIKI, XKCD]

def google_search(search_query: str, num_results: int, search_type: str) -> List[str]:
    """
    Return a list of search results by Google's search engine.

    List elements will be dictionaries with keys as below in the 'items' section:
    https://developers.google.com/custom-search/v1/cse/list#response
    """
    GOOGLE_SEARCH_API_KEY = os.environ['GOOGLE_SEARCH_API_KEY']
    logger.info("Received query: %s | num results: %s | search type: %s", search_query, num_results, search_type)
    logger.info(f"{type(search_type)}")

    res = requests.get(
        "https://www.googleapis.com/customsearch/v1",
        params={
            'key': GOOGLE_SEARCH_API_KEY,
            'q': search_query,
            'num': num_results,
            'cx': os.environ[f"GOOGLE_SEARCH_ENGINE_ID_{search_type.upper()}"],
        }
    ).json()

    # there is no 'items' key if there's an error or no results
    if 'error' in res or not int(res['searchInformation']['totalResults']):
        return []

    return res['items']


def search(search_type: str, inputs: List[str]) -> discord.Embed:
    """
    Return a formatted string from the given query in inputs and the search type.
    """
    logger.info("Searching - inputs: %s | type: %s", inputs, search_type)

    # default to one to prevent the bot's messages from taking too much space in chat
    # also notes if the result is fixed; by default it is not
    num_results = 1

    logger.info("post-process - inputs: %s | type: %s", inputs, search_type)

    results = google_search(inputs, num_results, search_type)

    if not results:
        return discord.Embed(title=NO_RESULTS_FOUND_MESSAGE)

    displayed_result = ''

    # Formatting appearance:
    # >>> !wiki apple
    #
    # Apple Inc. - Wikipedia
    #
    # Apple Inc. is an American multinational technology company headquartered in
    # Cupertino, California, that designs, develops, and sells consumer electronics, ...
    #
    # https://en.wikipedia.org/wiki/Apple_Inc
    for result in results:
        title = result['title']
        snippet = result['snippet']
        link = result['link']
        displayed_result += "**{}**\n{}\n{}\n\n".format(title, snippet, link)

    return discord.Embed(title="Top search results", description=displayed_result)
