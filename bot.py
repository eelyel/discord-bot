from log import logger
import discord
import os

BOT_TOKEN = os.environ['BOT_TOKEN']
COMMAND_PREFIXES = ["!", "$", "`"]

client = discord.Client()

@client.event
async def on_ready():
    logger.debug(f"Logged in as: {client.user.name} ({client.user.id})")

@client.event
async def on_message(message):
    pass

client.run(BOT_TOKEN)
