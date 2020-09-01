# -*- coding: utf-8 -*-
"""
This module maintains some constants for using the Froxy module.

Constants:

    API_URL: str - URL to get data from proxies;

    PROXIES_DATA_REGEX: re.Pattern - Regex compiled to get from proxies.
        Data:
            ├─ IP
            ├─ Separator
            ├─ Port
            ├─ Separator (space)
            └─ Proxy information
                ├─ Anonymity [N|A|H]
                ├─ Type [ |S|!]
                └─ Google passed [-|+]

"""

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

HTTP_FLAGS: list = ['', '!']

HTTPS_FLAGS: list = ['S', 'S!']