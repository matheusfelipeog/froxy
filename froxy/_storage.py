# -*- coding: utf-8 -*-


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
