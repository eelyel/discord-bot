from discord.ext import commands
from log import logger
from random import randint
import discord
import os
import searches


bot = commands.Bot(command_prefix=["!", "`"])
BOT_TOKEN = os.environ['BOT_TOKEN']

COIN = ['HEADS', 'TAILS']
SEARCH_FUNCTION_TEMPLATE = """
@bot.command()
async def {0}(ctx, *args):
    await ctx.send(embed=searches.search('{0}', *args))
"""

HELP_MESSAGE = """
    Precede the following with any of `, !, $
    **Misc**
    help
    roll <Number|NdM|abc>

    **Searches**
    <mal|md|mu|nu|scp|wiki|xkcd>[#][^][#] <search query>
    """


@bot.listen()
async def on_ready():
    logger.info("Logged in as: %s (%s)", bot.user.name, bot.user.id)


@bot.listen()
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


async def show_help() -> discord.Embed:
    return discord.Embed(description=HELP_MESSAGE)


@bot.command()
async def kill(_, __):
    while 1:
        pass


@bot.command()
async def perm(ctx, *args):
    """
    Return a permutated sequence of the given number, or of the given input
    """
    inputs = list(*args)
    logger.info("Going to permutate %s", inputs)

    if len(inputs) == 1:
        try:
            inputs = [i for i in range(1, len(inputs[0]) + 1)]
        except ValueError:
            pass

    logger.info("Permutating %s", inputs)
    rand_inputs = []

    while inputs:
        rand_pos = randint(0, len(inputs) - 1)
        rand_inputs.append(inputs[rand_pos])
        del inputs[rand_pos]

    await ctx.send(rand_inputs)


@bot.command()
async def roll(ctx, *args):
    """
    Return a randomized number or selection, based on the format of input.

    # >>> roll(['Alice', 'Bob', 'Charlie'])
    # 'Bob'

    # >>> roll(['6'])
    # '3'

    # >>> roll(['2d20'])
    # '(15) + (3) = 18'
    """
    inputs = list(*args)
    logger.info("Rolling - inputs: %s", inputs)

    if len(inputs) > 1:
        # !roll Alice Bob Charlie - random string list rolling
        await ctx.send(inputs[randint(0, len(inputs) - 1)])
        return

    inp = inputs[0]
    # !roll 10 - standard n-sided roll
    if inp.isdigit() and int(inp) > 0:
        await ctx.send(randint(1, int(inp)))
        return

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
        await ctx.send(inp)
        return

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
    await ctx.send(total_str)


@bot.command()
async def flip(ctx, *args):
    inputs = list(*args)
    logger.info("Flipping %s", inputs)
    if len(inputs) == 2:
        await ctx.send(inputs[randint(0, 1)])
        return

    await ctx.send(COIN[randint(0, 1)])


# dynamically create commands for search sites
for site in searches.ALL_SITES:
    logger.info("Creating functions: %s", site)
    exec(SEARCH_FUNCTION_TEMPLATE.format(site))

bot.run(BOT_TOKEN)
