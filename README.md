# Discord Bot

A Discord bot with several available capabilities such as dice rolls and text-embedded search queries for multiple websites.

## Prerequisites

### Python

Python version 3.5.3 or above is required as the discord.py library requires it above that version.

### Python libraries

Currently one library is needed to run the bot itself, and another for testing:

discord.py is used as a wrapper for the Discord API. Installation instructions are as in [here](https://pypi.org/project/discord.py/):

```
python3 -m pip install -U discord.py[voice]
```

pytest is used as an alternative to the default unittest module. Installation instructions are as in [here](https://docs.pytest.org/en/latest/getting-started.html):

```
python3 -m pip install -U pytest
```

To run the tests, do

```
pytest test.py
```

### Environmental variables

Currently the Discord bot token as well as the google search engine ids are set via environmental variables. Remove or comment out the instance in commands.py and searches.py if the command is unneeded.

### Planned features

Message saving, user pinging, unit tests (in progress), github CI/CD
