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

from .__about__ import __version__
from .__about__ import __author__
from .__about__ import __email__
from .__about__ import __github__

__version__ = __version__
__author__ = f'{__author__} <{__email__}> and <{__github__}>'

__all__ = ['Froxy']

from ._froxy import Froxy as Froxy
