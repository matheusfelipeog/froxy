# -*- coding: utf-8 -*-

# --- Standard libraries ----
import sys
import re

# --- Third-party libraries ---
import requests

# --- Local libraries ---
from ._const import API_URL

from ._const import PROXIES_DATA_REGEX

from ._const import HTTP_FLAGS, HTTPS_FLAGS


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
                Froxy._split_proxy_info(
                    d[2].strip(' ')  # Proxy Info
                )  
            ]
            for d in data
        ]

    @staticmethod
    def _split_proxy_info(data: str) -> list:
        
        country = data[:2]
        anonymity = data[3:4]
        type_ = data[4:].strip('-+ ')  # Remove splitting (- and space) and google_passed flag (+)
        google_passed = data[-1]

        return [country, anonymity, type_, google_passed]

    def _set_proxies_in_storage(self) -> None:

        data_raw = self._get_data_in_api(API_URL)

        self._proxy_storage = self._data_normalization(data_raw)

    def _base_proxies_filter(self, filters: list) -> list:
        
        return list(
            filter(
                lambda proxies: proxies[2][2] in filters,
                self._proxy_storage
            )
        )

    def http(self) -> list:
        return self._base_proxies_filter(HTTP_FLAGS)

    def https(self) -> list:
        return self._base_proxies_filter(HTTPS_FLAGS)

    def get(
            self,
            country: str=None,
            anonymity: str=None,
            protocol: str=None,
            google_passed: str=None
        ) -> list:
        
        # if don't have a filter flag, return all proxies.
        if not any([country, anonymity, protocol, google_passed]):
            return self._proxy_storage

        proxies = []  # Storage of filtered proxies

        # Normalize
        if country and isinstance(country, str):
            country = country.upper()

        if anonymity and isinstance(anonymity, str):
            anonymity = anonymity.upper()
        
        if protocol and isinstance(protocol, str):
            protocol = protocol.lower()

            # -- Protocol Flag --
            if protocol == 'http':
                proxies.extend(self.http())
            elif protocol == 'https':
                proxies.extend(self.https())
        
        if google_passed and isinstance(google_passed, str):
            google_passed = google_passed.upper()
        
        return proxies

    def start(self):
        self._set_proxies_in_storage()

        return self
