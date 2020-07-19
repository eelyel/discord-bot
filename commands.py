from functools import partial
from log import logger
from random import randint
from searches import search
from typing import List
import discord
import searches


ALL_COMMANDS = {
    'help': lambda *_: show_help(),
    'kill': None,
    'roll': lambda _, inputs, cid: roll(inputs),
    searches.MAL: partial(search, searches.MAL),
    searches.MD: partial(search, searches.MD),
    searches.MU: partial(search, searches.MU),
    searches.NU: partial(search, searches.NU),
    searches.SCP: partial(search, searches.SCP),
    searches.STEAM: partial(search, searches.STEAM),
    searches.WIKI: partial(search, searches.WIKI),
    searches.XKCD: partial(search, searches.XKCD),
}

HELP_MESSAGE = """
    Precede the following with any of `, !, $
    **Misc**
    help
    roll <Number|NdM|abc>

    **Searches**
    <mal|md|mu|nu|scp|wiki|xkcd>[#][^][#] <search query>
    """


def show_help() -> discord.Embed:
    return discord.Embed(description=HELP_MESSAGE)


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
