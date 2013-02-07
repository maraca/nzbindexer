"""
Used to route to the correct Regex.
"""

__author__ = 'cozzi.martin@gmail.com'

import re

from regexes.constants import REGEXES


class RegexRouter:
    """Routes a group to a list of regexes."""

    def __init__(self, group, autoload=True):
        """Inits the router for a specific group"""
        self.group = group
        self.patterns = []
        if autoload:
            self.patterns = self.load_all_compiled()

    def load_all_compiled(self):
        """Returns all the regexes associated with a group."""
        return [re.compile(regex) for regex in REGEXES.get(self.group.name)]

    def parse(self, data):
       for pattern in self.patterns:
           result = pattern.search(data)
           if result:
               return result

       return None
