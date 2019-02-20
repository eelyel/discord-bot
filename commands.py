"""Core logic implementation of commands."""

from typing import Set, List
from random import randint
import discord
from log import logger
from search import Search


ALL_COMMANDS = {
    'help': lambda *_: show_help(),
    # pylint: disable=unnecessary-lambda
    # Required due to referencing function prior to declaration
    'ping': lambda args, inputs: ping(args, inputs),
    'roll': lambda _, inputs: roll(inputs),
    'scp': lambda args, inputs: search(args, inputs, Search.SCP),
    'mal': lambda args, inputs: search(args, inputs, Search.MAL),
    'md': lambda args, inputs: search(args, inputs, Search.MD),
    'mu': lambda args, inputs: search(args, inputs, Search.MU),
    'nu': lambda args, inputs: search(args, inputs, Search.NU),
    'wiki': lambda args, inputs: search(args, inputs, Search.WIKI),
    'xkcd': lambda args, inputs: search(args, inputs, Search.XKCD),
}

def show_help() -> str:
    """
    Return a help string.
    """
    return discord.Embed(
        description="""Precede the following with any of `, !, $
                    **Misc**
                    help
                    ping
                    roll <Number|NdM|abc>


                    **Searches**
                    scp[#]  <number|search query>
                    <mal|md|mu|nu|wiki|xkcd>[#] <search query>"""
        )

def ping(args: Set[str], inputs: List[str]) -> str:
    """
    Return a formatted string of IDs to be pinged.
    """
    logger.info("Pinging - args: %s | inputs: %s", args, inputs)
    return ''

def roll(inputs: List[str]) -> str:
    """
    Return a randomized number or selection, based on the format of input.

    >>> roll(['Alice', 'Bob', 'Charlie'])
    'Bob'

    >>> roll(['6'])
    '3'

    >>> roll(['2d20'])
    '(15) + (3) = 18'

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
        # !roll 10
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
        # !roll 2d20
        total = 0
        total_str = ''
        while num > 0:
            ran = randint(1, side)
            total += ran
            total_str += f"({ran}) + "
            num -= 1
        total_str = total_str[:-2] + '= ' + str(total)
        return total_str

    # !roll Alice Bob Charlie
    return inputs[randint(0, len(inputs) - 1)]

def search(args: Set[str], inputs: List[str], search_type: Search) -> str:
    """
    Return a formatted string from the given query in inputs and the search type.
    """
    logger.info("Searching - args: %s | inputs: %s | type: %s", args, inputs, search_type)
    return ''
