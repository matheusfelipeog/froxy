# -*- coding: utf-8 -*-
"""
Module for getting and filtering proxies.

This module consumes the API located at: https://github.com/clarketm/proxy-list and
filters data and provides an interface for using proxies.

Example:
```
>>> from froxy import Froxy
>>> froxy = Froxy()
>>> froxy.get()
# Output
[['255.255.255.255', '3000', ['US', 'N', 'S!', '+'], ...]
```
"""

__all__ = ['Froxy']

from ._froxy import Froxy as Froxy
