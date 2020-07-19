from commands import show_help, roll
from functools import partial
from log import logger
from searches import search
from typing import List
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


# pylint: disable=invalid-name
# Disabled due to style
client = discord.Client()


@client.event
async def on_ready():
    """
    Called usually after a successful login;
    may not be the first to be called, and also may not be called just once
    """
    logger.info("Logged in as: %s (%s)", client.user.name, client.user.id)


@client.event
async def on_message(message):
    """Called when a message is created and sent to a server"""
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
        logger.info("function is awaitable")
        msg = await fnc(args, inputs, message.channel.id)
    else:
        logger.info("function is not awaitable")
        msg = fnc(args, inputs, message.channel.id)

    if isinstance(msg, discord.Embed):
        await channel.send(embed=msg)
    elif msg:
        await channel.send(msg)


@client.event
async def on_reaction_add(reaction, user):
    """
    Called when a message has a reaction added to it
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
            logger.info("Failed to delete message %s", message_info)


def parse_command(content: str) -> (str, List[str], List[str]):
    """
    Return a message content's command, arguments, and inputs.

    >>> parse_command("!wiki")
    ('wiki', [], [])

    >>> parse_command("`wiki12nil hello and bye")
    ('wiki', {'1', '2', 'n', 'i', 'l'}, ['hello', 'and', 'bye'])

    # the ^ indicates to the command that it should take its inputs from previous server messages
    >>> parse_command("`$wiki1^2")
    ('wiki', {'1', '^2'})
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
    # extract the ^ (search character) and merge it with the number if applicable (['^', '1'] -> ['^1'])
    # if there is no number immediately following the ^, then ignore the character following it
    s_char = '^'
    try:
        pos = args.index(s_char)
        if args[pos + 1].isdigit():
            args[pos] = args[pos] + args[pos + 1]
            del args[pos + 1]
    except (ValueError, IndexError):
        # char may not exist, or may not have a valid tracing character
        # either way, no need to touch the arguments
        pass
    return command, args, split_content[1:]


client.run(BOT_TOKEN)
