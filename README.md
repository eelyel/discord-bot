
# Discord Bot [![Build Status](https://travis-ci.org/slateny/discord-bot.svg?branch=master)](https://travis-ci.org/slateny/discord-bot)

A Discord bot with several available capabilities such as dice rolls and text-embedded search queries for multiple websites.

## Prerequisites

### Python

Python version 3.5.3 or above is required as the discord.py library requires it above that version.

### Python libraries

The following libraries are required:

discord.py is used as a wrapper for the Discord API. Installation instructions are as in [here](https://pypi.org/project/discord.py/):

```
python3 -m pip install -U discord.py[voice]
```

The requests library is used for API calls:

```
python3 -m pip install -U requests
```

pytest is used as an alternative to the default unittest module. Installation instructions are as in [here](https://docs.pytest.org/en/latest/getting-started.html):

```
python3 -m pip install -U pytest
```

AWS Lambda is used, which relies on a system call to the [AWS CLI](https://aws.amazon.com/cli/):

```
python3 -m pip install -U awscli
```

To run the tests, do

```
pytest test.py
```

### Environmental variables

Currently the Discord bot token as well as the Google search engine ids are set via environmental variables. Remove or comment out the instance in commands.py and searches.py if the command is unneeded.

### Planned features

Message saving
