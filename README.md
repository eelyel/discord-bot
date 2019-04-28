# Discord Bot

A Discord bot with several available capabilities such as dice rolls, text-embedded search queries for multiple websites, and user pinging (WIP).

## Prerequisites

### Python

Python version 3.5.3 or above is required as the discord.py library requires it above that version.

### Python libraries

Currently only one library is needed to run the bot:

discord.py is used as a wrapper for the Discord API. Installation instructions are as in [here](https://pypi.org/project/discord.py/):

```
python3 -m pip install -U discord.py[voice]
```

### Environmental variables

Currently the Discord bot token as well as the google search engine ids are set via environmental variables. Remove or comment out the instance in commands.py and searches.py if the command is unneeded.
