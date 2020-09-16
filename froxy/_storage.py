# -*- coding: utf-8 -*-
"""Module for storage and data manipulation of Froxy class."""

# --- Standard libraries ----
from copy import deepcopy


class Storage(object):
    """Class for storage and data manipulation of Froxy class."""

    def __init__(self):
        
        # Internal use
        self._storage = []

        # Public use
        self.length = 0
    
    def __str__(self):
        return f'The storage contains {self.length} data saved temporarily.'

    def __repr__(self):
        return f'Storage(storage_type={type(self._storage)}, length=<{self.length}>)'

    def insert(self, data: list) -> None:
        """Store data copy in memory temporarily.
        
        Key arguments:

        `data: list` - List of data for temporary storage.
        """

        self._storage.extend(
            deepcopy(data)
        )

        self.length += len(data)
    
    def get(self) -> list:
        """Get a copy of all data in the temporary memory."""

        return deepcopy(
            self._storage
        )

    def generator(self):
        """Get a copy of the data in temporary memory in generator format."""

        for data in deepcopy(self._storage):
            yield data

    def clear(self) -> None:
        """Force clear temporary storage."""

        self._storage.clear()
