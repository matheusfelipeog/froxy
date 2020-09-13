# -*- coding: utf-8 -*-

# --- Standard libraries ----
from copy import deepcopy


class Storage(object):
    """Class for storage and data manipulation."""

    def __init__(self):
        
        # Internal use
        self._storage = []

        # Public use
        self.length = 0
    
    def __str__(self):
        return f'The storage contains {self.length} data saved temporarily.'

    def __repr__(self):
        return f'class Storage(storage_type={type(self._storage)}, length=<{self.length}>)'

    def insert(self, data: list) -> None:
        """Store data copy in memory temporarily.
        
        Key arguments:

        `data: list` - List of data for temporary storage.
        """

        self._storage.extend(
            deepcopy(data)
        )

        self.length += len(data)
