# -*- coding: utf-8 -*-

# Standard libraries
import sys
import re

# Third-party libraries
import requests

# Local libraries
from ._const import API_URL, PROXIES_DATA_REGEX


class Froxy(object):
    
    def __init__(self):

        self._proxy_storage: list = []

    def _get_data_in_api(self, url: str) -> list:

        try:
            resp = requests.request('GET', url, timeout=10)
            resp.raise_for_status

            return self._data_filter(resp.text)

        except (requests.ConnectionError, requests.ConnectTimeout, requests.HTTPError) as err:
            sys.exit(err)
            
    def _data_filter(self, data: str) -> list:

        return PROXIES_DATA_REGEX.findall(str(data))

    def _data_normalization(self, data: list) -> list:

        return [ 
            [
                d[0],  # IP
                d[1],  # Port
                self._split_proxy_info(
                    d[2].strip(' ')  # Proxy Info
                )  
            ]
            for d in data
        ]

    def _split_proxy_info(self, data: str) -> list:
        
        country = data[:2]
        anonymity = data[3:4]
        type_ = data[4:].strip('-+ ')  # Remove splitting (- and space) and google_passed flag (+)
        google_passed = data[-1]

        return [country, anonymity, type_, google_passed]

    def _set_proxies_in_storage(self) -> None:

        data_raw = self._get_data_in_api(API_URL)

        self._proxy_storage = self._data_normalization(data_raw)

    def start(self):
        self._set_proxies_in_storage()

        return self

    def proxy_list(self) -> list:
        return self._proxy_storage
