import os
import logging

'''
Source: https://docs.python.org/2/howto/logging.html#logging-basic-tutorial

Level	When it’s used
----------------------
DEBUG      Detailed information, typically of interest only when diagnosing problems.
INFO       Confirmation that things are working as expected.
WARNING    An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
ERROR      Due to a more serious problem, the software has not been able to perform some function.
CRITICAL   A serious error, indicating that the program itself may be unable to continue running.
'''
LOG_FILE = 'discord.log'

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
