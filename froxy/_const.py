# -*- coding: utf-8 -*-
"""
This module maintains some constants for using the Froxy module.

Constants:

    API_URL: str - URL to get data from proxies;

    PROXIES_DATA_REGEX: re.Pattern - Regex compiled to get from proxies;
        Data:
            ├─ IP
            ├─ Separator
            ├─ Port
            ├─ Separator (space)
            └─ Proxy information
                ├─ Anonymity [N|A|H]
                ├─ Type [ |S|!]
                └─ Google passed [-|+]
    

    ------------------ FLAGS ------------------

    COUNTRY_CODE_FLAGS_REGEX: re.Pattern -  Country Code - ISO 3166-1 alpha-2;
        └─ More info in: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

    ANONYMITY_FLAGS: list - Proxy Anonymity is splitting in three flags (N, A, H);
        └─ Flags:
            ├─ N - No anonymity
            ├─ A - Anonymity
            └─ H - High anonymity

    HTTP_FLAGS: list - Flags for http protocol;

    HTTPS_FLAGS: list - Flags for https protocol.

    GOOGLE_PASSED_FLAGS: list - Google proxy.
        ├─  A Google proxy (also known as the google-passed proxy)
        │   is an HTTP proxy which has the following two features:
        │      ├─ 1. It must support searching on Google and a Google
        │      │     proxy should support HTTPS/SSL;
        │      └─ 2. Google must not block it.
        │
        ├─ Flags:
        │   ├─ (+) - Yes
        │   └─ (-) - No
        │
        └─ More info in: https://free-proxy-list.net/blog/google-proxies-dead


For more info about Flags, see: https://github.com/clarketm/proxy-list
"""

from .__about__ import __version__
from .__about__ import __author__
from .__about__ import __email__
from .__about__ import __github__

__version__ = __version__
__author__ = f'{__author__} <{__email__}> and <{__github__}>'

import re

API_URL: str = "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt"

PROXIES_DATA_REGEX: re.Pattern = re.compile(r'''
    (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})  # IP
    :                                  # Separator
    (\d{0,5})                          # Port
    \s                                 # Separator (space)
    ([A-Z\- \-\+!]+)                   # Proxy information
                                       #   ├─ Anonymity [N|A|H]
                                       #   ├─ Type [ |S|!]
                                       #   └─ Google passed [-|+]
''', re.VERBOSE)

# Country Code - ISO 3166-1 alpha-2 <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>
COUNTRY_CODE_FLAGS_REGEX: re.Pattern = re.compile(r'^([A-Z]{2})')

ANONYMITY_FLAGS: list = ['N', 'A', 'H']

# Protocol Flag
HTTP_FLAGS: list = ['', '!']
HTTPS_FLAGS: list = ['S', 'S!']

GOOGLE_PASSED_FLAGS: list = ['-', '+']
