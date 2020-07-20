from log import logger
from random import randint
from typing import List
import discord
import os
import requests

NO_RESULTS_FOUND_MESSAGE = "No results found"

MAL = 'MAL'
MD = 'MD'
MU = 'MU'
NU = 'NU'
SCP = 'SCP'
STEAM = 'STEAM'
WIKI = 'WIKI'
XKCD = 'XKCD'


def google_search(search_query: str, num_results: int, search_type: str) -> List[str]:
    """
    Return a list of search results by Google's search engine.

    List elements will be dictionaries with keys as below in the 'items' section:
    https://developers.google.com/custom-search/v1/cse/list#response
    """
    GOOGLE_SEARCH_API_KEY = os.environ['GOOGLE_SEARCH_API_KEY']

    res = requests.get(
        "https://www.googleapis.com/customsearch/v1",
        params={
            'key': GOOGLE_SEARCH_API_KEY,
            'q': search_query,
            'num': num_results,
            'cx': os.environ[f"GOOGLE_SEARCH_ENGINE_ID_{search_type}"],
        }
    ).json()

    # there is no 'items' key if there's an error or no results
    if 'error' in res or not int(res['searchInformation']['totalResults']):
        return []

    return res['items']


def search(search_type: str, args: List[str], inputs: List[str], channel_id: int) -> discord.Embed:
    """
    Return a formatted string from the given query in inputs and the search type.
    """
    logger.info("Searching - args: %s | inputs: %s | type: %s", args, inputs, search_type)

    # default to one to prevent the bot's messages from taking too much space in chat
    # also notes if the result is fixed; by default it is not
    num_results = 1

    # Look for any numerical argument passed in; arbitrarily choose one
    # it will represent the number of search results to return (it will never be > 10)
    # look also for 'r': this represents a random number between 1-5000 - specifically for SCP
    for arg in args:
        if arg.isdigit():
            # capped results at 5 to prevent more than 2000 chars being sent at once (400 exception)
            num_results = min(int(arg), 5)
            logger.info("Changing number of search results to %i", num_results)
        if 'r' in arg:
            # allow results to be 3
            num_results = 3
            scp_num = str(randint(1, 5000))
            inputs.append(scp_num)
            logger.info("Appended %s to inputs: %s", scp_num, inputs)
            break

    inputs = ' '.join(inputs)
    logger.info("post-process - args: %s | inputs: %s | type: %s", args, inputs, search_type)

    results = google_search(inputs, num_results, search_type)

    if not results:
        return NO_RESULTS_FOUND_MESSAGE

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
