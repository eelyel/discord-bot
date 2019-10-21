"""Core logic implementation of commands."""
from bufferlist import Buffer_List
from typing import List
from random import randint
import discord
from log import logger
import searches
import re
import requests
from zipfile import ZipFile
from subprocess import Popen
import uuid
import os
import asyncio


ALL_COMMANDS = {
    'help': lambda *_: show_help(),
    'kill': None,
    'roll': lambda _, inputs, cid: roll(inputs),
    'zip': lambda _, inputs, cid: comic_zip(inputs),
    searches.SCP: lambda args, inputs, cid: search(args, inputs, searches.SCP, cid),
    searches.STEAM: lambda args, inputs, cid: search(args, inputs, searches.STEAM, cid),
    searches.MAL: lambda args, inputs, cid: search(args, inputs, searches.MAL, cid),
    searches.MD: lambda args, inputs, cid: search(args, inputs, searches.MD, cid),
    searches.MU: lambda args, inputs, cid: search(args, inputs, searches.MU, cid),
    searches.NU: lambda args, inputs, cid: search(args, inputs, searches.NU, cid),
    searches.WIKI: lambda args, inputs, cid: search(args, inputs, searches.WIKI, cid),
    searches.XKCD: lambda args, inputs, cid: search(args, inputs, searches.XKCD, cid),
}

BUFFER_MESSAGES = Buffer_List()

def show_help() -> discord.Embed:
    """
    Return a help string.
    """
    return discord.Embed(
        description="""Precede the following with any of `, !, $
                    **Misc**
                    help
                    roll <Number|NdM|abc>
                    zip <url>

                    **Searches**
                    <mal|md|mu|nu|scp|wiki|xkcd>[#][^][#] <search query>"""
        )

def roll(inputs: List[str]) -> str:
    """
    Return a randomized number or selection, based on the format of input.

    # >>> roll(['Alice', 'Bob', 'Charlie'])
    # 'Bob'

    # >>> roll(['6'])
    # '3'

    # >>> roll(['2d20'])
    # '(15) + (3) = 18'

    >>> roll([''])
    ''

    >>> roll(['abc'])
    'abc'
    """
    logger.info("Rolling - inputs: %s", inputs)
    if not inputs:
        return ''

    if len(inputs) == 1:
        inp = inputs[0]
        # !roll 10 - standard n-sided roll
        if inp.isdigit() and int(inp) > 0:
            return str(randint(1, int(inp)))

        try:
            # Fails when there is no 'd': !roll abc
            (num, side) = inp.split('d')[:2]
            # Both fail on strings: !roll 1dc
            num = int(num)
            side = int(side)
            if num <= 0:
                logger.info("num is nonpositive: %s", num)
                raise ValueError("num must be positive!")
            if side <= 0:
                logger.info("side is nonpositive: %s", side)
                raise ValueError("side must be positive!")
        except ValueError:
            # !roll abc or !roll 1dc
            logger.info("Rolling 1 input dice %s", inp)
            return inp

        logger.info("Rolling dnd dice with num %s and side %s", num, side)
        # !roll 2d20 - DnD style rolling
        total = 0
        total_str = ''
        while num > 0:
            ran = randint(1, side)
            total += ran
            total_str += f"({ran}) + "
            num -= 1
        total_str = total_str[:-2] + '= ' + str(total)
        return total_str

    # !roll Alice Bob Charlie - random string list rolling
    return inputs[randint(0, len(inputs) - 1)]

async def comic_zip(inputs: List[str]) -> discord.Embed:
    """
    Return a message of the uploaded zip file containing the enhanced images from alphapolis.
    """
    if not inputs:
        return

    url = inputs[0]
    logger.info("Received URL: %s", url)

    # no string formatting as single/double bracket type matters (json accepts only a particular type)
    payload = '{"site": "' + url + '"}'

    # verify there are no duplicates
    while 1:
        filepath = "/tmp/" + str(uuid.uuid4())
        if not os.path.isfile(filepath):
            break

    # offload processing to AWS lambda - code is in lambda.py
    logger.info("Sending payload %s to lambda, storing in %s", payload, filepath)
    p = Popen(['aws', 'lambda', 'invoke', '--function-name', 'alpha_zip', '--payload', payload, filepath])

    # allow a full minute for lambda to respond - sometimes the zip can get a bit large
    for i in range(60):
        if os.path.isfile(filepath):
            if not i:
                return
            break
        await asyncio.sleep(1)

    with open(filepath, 'r') as f:
        result = f.read()
    logger.info("Received %s", result)

    # /tmp/ may not be cleaned up until reboot, but EC2 won't reboot often so better to immediately remove
    os.remove(filepath)
    logger.info("Deleted %s", filepath)

    upload_url = re.search("(https:.*?\.zip)", result)
    logger.info("URL found: %s", upload_url)
    if upload_url:
        return discord.Embed(title=f"Zip of {url}:", description=upload_url[0])
    return "Unable to zip images - verify URL"

def search(args: List[str], inputs: List[str], search_type: str, channel_id: int) -> discord.Embed:
    """
    Return a formatted string from the given query in inputs and the search type.
    """
    logger.info("Searching - args: %s | inputs: %s | type: %s", args, inputs, search_type)

    inputs = ' '.join(inputs)

    # default to one to prevent the bot's messages from taking too much space in chat
    num_results = 1

    # Look for any numerical argument passed in; arbitrarily choose one
    # it will represent the number of search results to return (it will never be > 10)
    # also look for ^, the character for indicating we should use recent messages from the chat
    for arg in args:
        if arg.isdigit():
            arg_int = int(arg)
            # capped results at 5 to prevent more than 2000 chars being sent at once (400 exception)
            num_results = 5 if arg_int > 5 else arg_int
            logger.info("Changing number of search results to %i", num_results)
        if arg.startswith('^'):
            logger.info("Searching via past messages")
            try:
                inputs = BUFFER_MESSAGES.get(channel_id, int(arg[1]))
                logger.info("Searching via past message of %s", inputs)
            except IndexError:
                # if indeed the ^ command is accompanied with no additional argument
                inputs = BUFFER_MESSAGES.get(channel_id, 0)
                logger.info("Failed to retrieved specified message, now searching for %s", inputs)

    results = searches.google_search(inputs, num_results, search_type)

    if not results:
        return "No results found - please verify spelling"

    displayed_result = ''

    # Formatting looks as follows:
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
