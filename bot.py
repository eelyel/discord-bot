from log import logger
import discord
import os
from typing import Set

BOT_TOKEN = os.environ['BOT_TOKEN']
COMMAND_PREFIXES = ["!", "$", "`"]
ALL_COMMANDS = ['help', 'roll', 'test', 'scp', 'md', 'nu', 'mu', 'mal', 'wiki', 'xkcd']

client = discord.Client()

@client.event
async def on_ready():
    logger.debug(f"Logged in as: {client.user.name} ({client.user.id})")

@client.event
async def on_message(message):
    content = ' '.join(message.content.split())

    command, args = parse_command(content)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == '🎲':
        message = reaction.message
        message_info = f"{message.content} by {user.name} ({user.id})"
        logger.info(f"Attempting to delete message {message_info}")
        try:
            await client.delete_message(message)
        except discord.HTTPException:
            logger.info(f"Failed to delete message {message_info}")

def parse_command(content: str) -> (str, Set[str]):
    """
    Return a message content's command and arguments.
    
    >>> parse_command('!wiki')
    ('wiki', set())

    >>> parse_command('`wiki12nil')
    ('wiki', {'1', '2', 'n', 'i', 'l'})
    """
    if content[0] not in COMMAND_PREFIXES:
        return None, None

    # !wiki5abc oranges -> wiki5abc
    unparsed_command = content.split()[0][1:]

    commands = list(filter(lambda COMMAND: unparsed_command.startswith(COMMAND), ALL_COMMANDS))

    if len(commands) == 0:
        return None, None

    # Take the first command regardless of multiple matches
    command = commands[0]
    args = set(unparsed_command[len(command):])
    return command, args


client.run(BOT_TOKEN)
