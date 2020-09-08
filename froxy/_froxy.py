# -*- coding: utf-8 -*-
"""
Module for getting and filtering proxies.

This module consumes the API located at: https://github.com/clarketm/proxy-list and
filters data and provides an interface for using proxies.

Usage:
```
>>> from froxy import Froxy
>>> froxy = Froxy()
>>> froxy.get()
# Output
[['255.255.255.255', '3000', ['US', 'N', 'S!', '+'], ...]
```
"""

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

        # Start for get data in API and set in storage
        self._set_proxies_in_storage()

    def _get_data_in_api(self, url: str) -> list:
        """Makes the api request and returns a list of filtered proxies.

        Keyword arguments:

        `url: str` - Proxies API address.
        """

        try:
            resp = requests.request('GET', url, timeout=10)
            resp.raise_for_status

            return self._data_filter(resp.text)

        except (requests.ConnectionError, requests.ConnectTimeout, requests.HTTPError, requests.ReadTimeout) as err:
            sys.exit(err)
            
    def _data_filter(self, data: str) -> list:
        """Filter data using regex and return the data list.

        Keyword arguments:

        `data: str` - Raw data of proxies.
        """

        return PROXIES_DATA_REGEX.findall(str(data))

    def _data_normalization(self, data: list) -> list:
        """Normalize proxy information to remove spaces and split information.

        Keyword arguments:

        `data: list` - List of raw proxies data.
        """

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
        """Split the proxy information and return a formatted list.

        Keyword arguments:

        `data: str` - Proxy information in string format. 
            Ex: "255.255.255.255:3000 AR-N-S! +"
        """
        
        country = data[:2]
        anonymity = data[3:4]
        type_ = data[4:].strip('-+ ')  # Remove splitting (- and space) and google_passed flag (+)
        google_passed = data[-1]

        return [country, anonymity, type_, google_passed]

    def _set_proxies_in_storage(self) -> None:
        """Save data in proxy storage."""

        data_raw = self._get_data_in_api(API_URL)

        self._proxy_storage = self._data_normalization(data_raw)

    def _base_proxies_filter(self, category: str, filters: list) -> list:
        """Filter proxies by category and flags.

        Keyword arguments:

        `category: str` - Proxy category [country, anonymity, protocol and google_passed].

        `filters: list` - Flags of filters.
        """

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
        """Filter model for reuse in `_base_proxies_filter(...)`.

        Keyword arguments:

        `data: list` - Complete list of proxies.

        `line: int` - Filter category line number.
        
        `col: int` - Filter category column number.
        
        `filters: list` - Flags of filters.
        """

        return filter(
            lambda proxies: proxies[line][col] in filters,
            data
        )

    def country(self, *flags: tuple) -> list:
        """Filter proxies for country.

        Use the country code to filter proxies.

        Keyword arguments:

        `flags: tuple` - Filter flags of selected countries.

        Code example:
            BR = Brazil
            US = United States of America
            EG = Egypt
            (...)

        See all codes at: [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

        Usage:
        ```
        >>> from froxy import Froxy
        >>> froxy = Froxy()
        >>> froxy.country('RS', 'US')
        # Example output
        [
            ['255.255.255.255', '3000', ['RS', 'N', 'S!', '-'], 
            ['254.254.254.254', '8058', ['US', 'N', 'S!', '+'],
            ...
        ]
        ```
        """

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
        """Filter proxies by anonymity level.

        Keyword arguments:

        `flags: tuple` - Filter flags of selected anonymity level.

        Anonymity levels:
            - Flags:
                - N = No anonymity
                - A = Anonymity
                - H = High anonymity

        Usage:
        ```
        >>> from froxy import Froxy
        >>> froxy = Froxy()
        >>> froxy.anonymity('A', 'H')
        # Example output
        [
            ['255.255.255.255', '3000', ['RS', 'H', 'S!', '-'], 
            ['254.254.254.254', '8058', ['US', 'A', 'S!', '+'],
            ...
        ]
        ```
        """

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
        """Filter proxies by http protocol.

        Usage:
        ```
        >>> from froxy import Froxy
        >>> froxy = Froxy()
        >>> froxy.http()
        # Example output
        [
            ['255.255.255.255', '3000', ['AA', 'H', '!', '-'], 
            ['254.254.254.254', '8058', ['ZZ', 'A', '', '+'],
            ...
        ]
        ```
        """

        return self._base_proxies_filter(category='protocol', filters=HTTP_FLAGS)

    def https(self) -> list:
        """Filter proxies by https protocol.

        Usage:
        ```
        >>> from froxy import Froxy
        >>> froxy = Froxy()
        >>> froxy.https()
        # Example output
        [
            ['255.255.255.255', '3000', ['AA', 'H', 'S!', '-'], 
            ['254.254.254.254', '8058', ['ZZ', 'A', 'S', '+'],
            ...
        ]
        ```
        """

        return self._base_proxies_filter(category='protocol', filters=HTTPS_FLAGS)

    def google(self, flag: str) -> list:
        """Filter proxies by google passed.

        Keyword arguments:

        `flags: tuple` - Filter flags of google passed.
            - (+) = Yes
            - (-) = No

        A Google proxy (also known as the google-passed proxy)
        is an HTTP proxy which has the following two features:
            - 1. It must support searching on Google and a Google
                 proxy should support HTTPS/SSL;
            - 2. Google must not block it.

            More info at: https://free-proxy-list.net/blog/google-proxies-dead

        Usage:
        ```
        >>> from froxy import Froxy
        >>> froxy = Froxy()
        >>> froxy.google('+')
        # Example output
        [
            ['255.255.255.255', '3000', ['AA', 'H', 'S!', '+'], 
            ['254.254.254.254', '8058', ['YY', 'N', '', '+'],
            ...
        ]
        ```
        """

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
        """Use multiple proxy filters or get all proxies if the filter arguments are empty.

        Keyword arguments:

        `country: list` - List of flags of selected countries.
            - More info at: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

        `anonymity: list` - List of flags of selected anonymity level. (N, A or H).

        `protocol: str` - Selected protocol (http or https).

        `google_passed: str` - Filter flags of google passed. (- or +).
        
        Usage:
        ```
        >>> from froxy import Froxy
        >>> froxy = Froxy()
        >>> froxy.get(
            country=['US', 'BR', 'RS'],
            anonymity=['A', 'H'],
            protocol='https',
            google_passed='+'
        )
        # Example output
        [
            ['255.255.255.255', '3000', ['US', 'H', 'S!', '+'], 
            ['255.255.255.254', '3000', ['US', 'A', 'S', '-'], 
            ['254.254.254.253', '8058', ['BR', 'A', 'S', '+'],
            ['254.254.254.252', '4058', ['RS', 'H', 'S!', '-']
            ...
        ]
        ```
        """

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
