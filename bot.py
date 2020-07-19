from commands import show_help, roll
from functools import partial
from log import logger
from searches import search
from typing import List, Set
import discord
import inspect
import os
import searches

BOT_TOKEN = os.environ['BOT_TOKEN']
COMMAND_PREFIXES = ["!", "$", "`"]
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


client = discord.Client()


@client.event
async def on_ready():
    logger.info("Logged in as: %s (%s)", client.user.name, client.user.id)


@client.event
async def on_message(message):
    content = ' '.join(message.content.split())
    channel = message.channel

    command, args, inputs = parse_command(content)
    if command is None:
        return

    # kill switch that hangs the bot
    if command == 'kill':
        logger.warning("Killing bot")
        while 1:
            pass

    fnc = ALL_COMMANDS[command]
    if inspect.isawaitable(fnc):
        msg = await fnc(args, inputs, message.channel.id)
    else:
        msg = fnc(args, inputs, message.channel.id)

    if isinstance(msg, discord.Embed):
        await channel.send(embed=msg)
    elif msg:
        await channel.send(msg)


@client.event
async def on_reaction_add(reaction, user):
    """
    Will not be called if the message isn't cached:
    that is, if the bot wasn't running when the message was sent
    """
    # Allow deletions of bot messages via reacting with 'die'
    if reaction.emoji == '🎲':
        message = reaction.message
        message_info = f"{message.content} by {user.name} ({user.id})"
        logger.info("Attempting to delete message %s", message_info)
        try:
            await message.delete()
        except discord.HTTPException:
            logger.warning("Failed to delete message %s", message_info)


def parse_command(content: str) -> (str, Set[str], List[str]):
    """
    Return a message content's command, arguments, and inputs.

    >>> parse_command("!wiki")
    ('wiki', [], [])

    >>> parse_command("`wiki12nil hello and bye")
    ('wiki', {'1', '2', 'n', 'i', 'l'}, ['hello', 'and', 'bye'])
    """
    if not content or content[0] not in COMMAND_PREFIXES:
        return None, None, None

    split_content = content.split()

    # !wiki5abc oranges -> wiki5abc
    unparsed_command = split_content[0][1:]

    commands = list(filter(unparsed_command.startswith, ALL_COMMANDS.keys()))

    if not commands:
        return None, None, None

    # Take the first command regardless of multiple matches
    command = commands[0]

    args = list(unparsed_command[len(command):])

    return command, args, split_content[1:]


client.run(BOT_TOKEN)
