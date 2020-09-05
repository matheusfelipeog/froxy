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
from ._const import COUNTRY_CODE_FLAGS
from ._const import ANONYMITY_FLAGS
from ._const import GOOGLE_PASSED_FLAGS


class Froxy(object):
    
    def __init__(self):

        self._proxy_storage: list = []

    def _get_data_in_api(self, url: str) -> list:

        try:
            resp = requests.request('GET', url, timeout=10)
            resp.raise_for_status

            return self._data_filter(resp.text)

        except (requests.ConnectionError, requests.ConnectTimeout, requests.HTTPError, requests.ReadTimeout) as err:
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

    def _base_proxies_filter(self, category: str, filters: list) -> list:
        
        data_filtered = []
        
        if category == 'country':
            data_filtered.extend(
                Froxy._filter_model(self._proxy_storage, line=2, col=0, filters=filters)
            )
        
        elif category == 'anonymity':
            data_filtered.extend(
                Froxy._filter_model(self._proxy_storage, line=2, col=1, filters=filters)
            )

        elif category == 'protocol':
            data_filtered.extend(
                Froxy._filter_model(self._proxy_storage, line=2, col=2, filters=filters)
            )
        
        elif category == 'google_passed':
            data_filtered.extend(
                Froxy._filter_model(self._proxy_storage, line=2, col=3, filters=filters)
            )

        return data_filtered

    @staticmethod
    def _filter_model(data: list, line: int, col: int, filters: list):
        return filter(
            lambda proxies: proxies[line][col] in filters,
            data
        )

    def country(self, *flags: tuple) -> list:

        # Normalize to uppercase
        flags = [f.upper() for f in flags]

        # Delete invalid flags
        for idx, flag in enumerate(flags):
            if flag not in COUNTRY_CODE_FLAGS:
                del flags[idx]

        # If there are no flags, returns an empty list to not perform a linear search
        if not flags:
            return []

        return self._base_proxies_filter(category='country', filters=flags)

    def anonymity(self, *flags: tuple) -> list:
        # Normalize to uppercase
        flags = [f.upper() for f in flags]

        # Delete invalid flags
        for idx, flag in enumerate(flags):
            if flag not in ANONYMITY_FLAGS:
                del flags[idx]

        # If there are no flags, returns an empty list to not perform a linear search
        if not flags:
            return []
        
        return self._base_proxies_filter(category='anonymity', filters=flags)

    def http(self) -> list:
        return self._base_proxies_filter(category='protocol', filters=HTTP_FLAGS)

    def https(self) -> list:
        return self._base_proxies_filter(category='protocol', filters=HTTPS_FLAGS)

    def google(self, flag: str) -> list:

        # Validation
        if flag not in GOOGLE_PASSED_FLAGS:
            return []
        
        return self._base_proxies_filter(category='google_passed', filters=[flag])

    def get(
            self,
            country: list=None,
            anonymity: list=None,
            protocol: str=None,
            google_passed: str=None
        ) -> list:
        
        # if don't have a filter flag, return all proxies.
        if not any([country, anonymity, protocol, google_passed]):
            return self._proxy_storage

        proxies = []  # Storage of filtered proxies

        # Verify options
        if country and isinstance(country, list):
            proxies.extend(self.country(*country))

        if anonymity and isinstance(anonymity, list):
            proxies.extend(self.anonymity(*anonymity))

        if protocol and isinstance(protocol, str):
            protocol = protocol.lower()

            # -- Check Protocol Flag --
            if protocol == 'http':
                proxies.extend(self.http())
            elif protocol == 'https':
                proxies.extend(self.https())
        
        if google_passed and isinstance(google_passed, str):
            proxies.extend(self.google(flag=google_passed))

        return proxies

    def start(self):
        self._set_proxies_in_storage()

        return self
