"""Parses Discord information and delegates function calls"""

from typing import Set, List
import os
from commands import ALL_COMMANDS
import discord
from log import logger

BOT_TOKEN = os.environ['BOT_TOKEN']
COMMAND_PREFIXES = ["!", "$", "`"]

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

    msg = ALL_COMMANDS[command](args, inputs)
    if isinstance(msg, discord.Embed):
        await client.send_message(channel, embed=msg)
    elif msg:
        await client.send_message(channel, msg)


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
            await client.delete_message(message)
        except discord.HTTPException:
            logger.info("Failed to delete message %s", message_info)

def parse_command(content: str) -> (str, Set[str], List[str]):
    """
    Return a message content's command, arguments, and inputs.

    >>> parse_command("!wiki")
    ('wiki', set(), [])

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
    args = set(unparsed_command[len(command):])
    return command, args, split_content[1:]


client.run(BOT_TOKEN)
