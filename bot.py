from log import logger
import discord
from typing import Set, List
import os
from commands import ALL_COMMANDS

BOT_TOKEN = os.environ['BOT_TOKEN']
COMMAND_PREFIXES = ["!", "$", "`"]

client = discord.Client()

@client.event
async def on_ready():
    logger.debug(f"Logged in as: {client.user.name} ({client.user.id})")

@client.event
async def on_message(message):
    content = ' '.join(message.content.split())
    channel = message.channel

    command, args, inputs = parse_command(content)
    if command is None:
        return

    client.send_message(channel, ALL_COMMANDS[command](args, inputs))


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

def parse_command(content: str) -> (str, Set[str], List[str]):
    """
    Return a message content's command and arguments.
    
    >>> parse_command('!wiki')
    ('wiki', set())

    >>> parse_command('`wiki12nil')
    ('wiki', {'1', '2', 'n', 'i', 'l'})
    """
    if len(content) == 0 or content[0] not in COMMAND_PREFIXES:
        return None, None, None

    # !wiki5abc oranges -> wiki5abc
    unparsed_command = content.split()[0][1:]

    commands = list(filter(lambda COMMAND: unparsed_command.startswith(COMMAND), ALL_COMMANDS.keys()))

    if commands:
        return None, None, None

    # Take the first command regardless of multiple matches
    command = commands[0]
    args = set(unparsed_command[len(command):])
    return command, args, content[1:] if len(content) > 1 else []


client.run(BOT_TOKEN)
