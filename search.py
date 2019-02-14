from enum import Enum
import os

class Search(Enum):
    MAL = 'mal'
    MD = 'md'
    MU = 'mu'
    NU = 'nu'
    SCP = 'scp'
    WIKI = 'wiki'
    XKCD = 'xkcd'

    GOOGLE_SEARCH_API_KEY = os.environ['GOOGLE_SEARCH_API_KEY']

    GOOGLE_SEARCH_ENGINE_IDS = {
        MAL: os.environ['GOOGLE_SEARCH_ENGINE_ID_MAL'],
        MD: os.environ['GOOGLE_SEARCH_ENGINE_ID_MD'],
        MU: os.environ['GOOGLE_SEARCH_ENGINE_ID_MU'],
        MU: os.environ['GOOGLE_SEARCH_ENGINE_ID_NU'],
        SCP: os.environ['GOOGLE_SEARCH_ENGINE_ID_SCP'],
        WIKI: os.environ['GOOGLE_SEARCH_ENGINE_ID_WIKI'],
        XKCD: os.environ['GOOGLE_SEARCH_ENGINE_ID_XKCD'],
    }

