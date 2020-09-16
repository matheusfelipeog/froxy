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
import random

# --- Third-party libraries ---
import requests

# --- Local libraries ---
from ._storage import Storage

from ._const import API_URL

from ._const import PROXIES_DATA_REGEX

from ._const import HTTP_FLAGS, HTTPS_FLAGS
from ._const import COUNTRY_CODE_FLAGS_REGEX
from ._const import ANONYMITY_FLAGS
from ._const import GOOGLE_PASSED_FLAGS


class Froxy(object):
    """A class for manipulating and filtering proxies.
    
    Location of API used: https://github.com/clarketm/proxy-list
    """
    
    def __init__(self):
        """Initialize storage attributes and start method to save to storage.
        
        Public Attribute:

        `storage: list` - Data storage and manipulation object
        """

        self.storage: list = Storage()

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

        except (
            requests.ConnectionError,
            requests.ConnectTimeout,
            requests.HTTPError,
            requests.ReadTimeout
        ) as err:
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

        self.storage.insert(
            self._data_normalization(data_raw)
        )

    def _base_proxies_filter(self, category: str, filters: list) -> list:
        """Filter proxies by category and flags.

        Keyword arguments:

        `category: str` - Proxy category [country, anonymity, protocol and google_passed].

        `filters: list` - Flags of filters.
        """

        data_filtered = []
        
        if category == 'country':
            data_filtered.extend(
                Froxy._filter_model(self.storage.get(), line=2, col=0, filters=filters)
            )
        
        elif category == 'anonymity':
            data_filtered.extend(
                Froxy._filter_model(self.storage.get(), line=2, col=1, filters=filters)
            )

        elif category == 'protocol':
            data_filtered.extend(
                Froxy._filter_model(self.storage.get(), line=2, col=2, filters=filters)
            )
        
        elif category == 'google_passed':
            data_filtered.extend(
                Froxy._filter_model(self.storage.get(), line=2, col=3, filters=filters)
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

    @staticmethod
    def _filter_n_proxies(n: int, flags: list, func_filter) -> list:
        """Filter N proxies for reuse in `get(...)`.
        
        Keyword arguments:

        `n: int` - Number of proxies.

        `flags: list` - List of flags for filter.
        
        `func_filter: function` - Filter function used.
        """

        proxies = []
        for flag in flags:
            data = func_filter(flag)
            data_length = len(data)
            
            proxies.extend(
                random.sample(data, n if n < data_length else data_length)
            )
        
        return proxies
    
    @staticmethod
    def _is_valid_country(flag: str) -> bool:
        """Check if country argument is valid.
        
        Keyword arguments:

        `flag: str` - A code country in ISO 3166-1 alpha-2 format.
        """

        return bool(
            COUNTRY_CODE_FLAGS_REGEX.findall(flag)
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

        # If the countries are valid, return those countries 
        # in capital letters. if not, ignore
        flags = [
            flag.upper() for flag in flags 
            if Froxy._is_valid_country(flag)
        ]

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

    def http(self, *args, **kwargs) -> list:
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

    def https(self, *args, **kwargs) -> list:
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

    def google(self, flag: str, *args, **kwargs) -> list:
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
            country: list=[],
            anonymity: list=[],
            protocol: list=[],
            google_passed: list=[]
        ) -> list:
        """Use multiple proxy filters or get all proxies if the filter arguments are empty.

        Keyword arguments:

        `country: list` - Number and List of flags of selected countries.
            - More info at: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

        `anonymity: list` - Number and List of flags of selected anonymity level. (N, A or H).

        `protocol: list` - Number and Selected protocol (http or https).

        `google_passed: list` - Number and Filter flags of google passed. (- or +).
        
        Usage:
        ```
        >>> from froxy import Froxy
        >>> froxy = Froxy()
        >>> froxy.get(
                country=[1, 'US', 'BR'],
                anonymity=[2, 'H'],
                protocol=[2, 'https'],
                google_passed=[1, '+']
            )
        # Example output
        [
            ['255.255.255.255', '3000', ['US', 'H', 'S!', '+'], 
            ['254.254.254.254', '8058', ['BR', 'A', 'S', '+'],
            ['254.254.254.253', '6000', ['TT', 'H', '', '-'],
            ['254.254.254.252', '4058', ['BR', 'H', '!', '-'],
            ['255.255.255.251', '3000', ['RS', 'H', 'S', '-'], 
            ['254.254.254.250', '7058', ['ZZ', 'H', 'S!', '-'],
            ['254.254.254.250', '7058', ['YY', 'N', '', '+']
        ]
        ```
        """

        # if don't have a filter flag, return all proxies.
        if not any([country, anonymity, protocol, google_passed]):
            return self.storage.get()

        proxies = []  # Storage of filtered proxies


        # --- FILTER COUNTRY ---
        if country and isinstance(country, list) and country[0] > 0:

            filtred = Froxy._filter_n_proxies(
                        n=country[0], 
                        flags=country[1:], 
                        func_filter=self.country
                    )

            proxies.extend(filtred)


        # --- FILTER ANONYMITY ---
        if anonymity and isinstance(anonymity, list) and anonymity[0] > 0:

            filtred = Froxy._filter_n_proxies(
                        n=anonymity[0], 
                        flags=anonymity[1:], 
                        func_filter=self.anonymity
                    )

            proxies.extend(filtred)


        # --- FILTER PROTOCOL (HTTP AND HTTPS) ---
        if protocol and isinstance(protocol, list) and protocol[0] > 0:

            if protocol[1].lower() == 'http':
                
                filtred = Froxy._filter_n_proxies(
                        n=protocol[0], 
                        flags=['http'], 
                        func_filter=self.http
                    )

                proxies.extend(filtred)

            elif protocol[1].lower() == 'https':

                filtred = Froxy._filter_n_proxies(
                        n=protocol[0], 
                        flags=['https'], 
                        func_filter=self.https
                    )

                proxies.extend(filtred)
        

        # --- FILTER GOOGLE PASSED ---
        if google_passed and isinstance(google_passed, list) and google_passed[0] > 0:

            filtred = Froxy._filter_n_proxies(
                        n=google_passed[0], 
                        flags=google_passed[1:], 
                        func_filter=self.google
                    )

            proxies.extend(filtred)

        # Returns all filtered proxies 
        return proxies
