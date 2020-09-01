# -*- coding: utf-8 -*-

# Standard libraries
import sys
import re

# Third-party libraries
import requests

# Local libraries
from .const import API_URL, PROXIES_DATA_REGEX


class Froxy(object):
    
    def __init__(self):

        self._proxy_storage: list = []

        self.number_of_proxies: int = 0

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
            tuple(
                map(str.strip, d)
            )
            for d in data
        ]

    def _split_proxy_info(self):
        ...

    def _set_proxies_in_storage(self) -> None:

        data_raw = self._get_data_in_api(API_URL)

        self._proxy_storage = self._data_normalization(data_raw)
        self.number_of_proxies = len(data_raw)

    def start(self):
        self._set_proxies_in_storage()

        return self

    def proxy_list(self) -> list:
        return self._proxy_storage
