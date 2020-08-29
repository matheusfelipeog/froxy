# -*- coding: utf-8 -*-
"""
This module maintains some constants for using the Froxy module.

Constants:

    API_URL: str - URL to get data from proxies.

    PROXIES_DATA_REGEX: re.compile - Regex compiled to get from proxies
                                        Data:
                                            # IP
                                            # Separator
                                            # Port
                                            # Separator (space)
                                            # Proxy information
                                            #     Anonymity [N|A|H]
                                            #     Type [ |S|!]
                                            #     Google passed [-|+]

"""

from re import compile, VERBOSE

API_URL: str = "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt"

PROXIES_DATA_REGEX = compile(r'''
    (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})  # IP
    :                                  # Separator
    (\d{0,5})                          # Port
    \s                                 # Separator (space)
    ([A-Z\- \-\+!]+)                   # Proxy information
                                       #   - Anonymity [N|A|H]
                                       #   - Type [ |S|!]
                                       #   - Google passed [-|+]
''', VERBOSE)
