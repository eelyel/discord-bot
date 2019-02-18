from log import logger
from search import Search
from typing import Set, List


ALL_COMMANDS = {
    'help': lambda *_: show_help,
    'ping': lambda args, inputs: ping,
    'roll': lambda args, inputs: roll,
    'scp': lambda args, inputs: search(args, inputs, Search.SCP),
    'mal': lambda args, inputs: search(args, inputs, Search.MAL),
    'md': lambda args, inputs: search(args, inputs, Search.MD),
    'mu': lambda args, inputs: search(args, inputs, Search.MU),
    'nu': lambda args, inputs: search(args, inputs, Search.NU),
    'wiki': lambda args, inputs: search(args, inputs, Search.WIKI),
    'xkcd': lambda args, inputs: search(args, inputs, Search.XKCD),
}

def show_help() -> str:
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

async def ping(args: Set[str], inputs: List[str]) -> str:
    pass

async def roll(args: Set[str], inputs: List[str]) -> str:
    pass

async def search(args: Set[str], inputs: List[str], search_type: Search) -> str:
    pass
