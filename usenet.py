"""
Provides an abstraction of Usenet's model to allow for
easy manipulation of the data coming from the remote host.
"""

import logging
import nntplib

from collections import namedtuple
from regexes import RegexRouter
from regexes.constants import REGEXES


LOGGER = logging.getLogger('usenet_indexer')


class UsenetManager:
    """Manages connections and tasks and such."""

    News = namedtuple('News', ['subject', 'message_id', 'segment'])
    NewsGroup = namedtuple('NewsGroup',
            ['response', 'count', 'first', 'last', 'name'])

    HEADER = 'Subject'

    def __init__(self, configs):
        """Inits itself."""
        self.configs = configs['usenet']
        self.connection = None
        self.group = self.NewsGroup(*(None, ) * 5)
        self.fishnet = {}

    def _connect(self):
        """Connects to a remote Usenet server"""
        LOGGER.info('New remote connection')
        connection = nntplib.NNTP(
                self.configs['host'],
                user=self.configs['user'],
                password=self.configs['password'])
        return connection

    def _get_connection(self):
        """Gives an existing connections, and reconnects if needed."""
        if self.connection:
            try:
                return self.connection
            except nntplib.NNTPPermanentError:
                LOGGER.debug('Connection timeout. Reconnecting.')
                self.connection = self._connect()
        else:
            self.connection = self._connect()

        LOGGER.info('Connected to %s as %s',
                self.configs['host'], self.configs['user'])
        LOGGER.info('Server says: "%s"', self.connection.getwelcome())

        return self.connection

    def _get_oldest_header(self):
        """Returns the oldest header inserted in the database."""
        pass

    def _get_most_recent_header(self):
        """Returns the most recent header inserted in the database."""
        pass

    def _get_xhdr_string(self, first, last):
        """Returns a string to query the Usenet server."""
        return '{0} - {1}'.format(first, last)

    def get_header_data(self, header):
        """Extracts the name and the part from a header"""
        article_number = header[0]
        data = self.router.parse(header[1])
        if data:
            data = data.groupdict()
            news = self.News(subject=data.get('name'),
                             message_id=self.get_message_id(article_number),
                             segment=data.get('parts'))

            if self.fishnet.get(data.get('name')) is None:
                self.fishnet[data.get('name')] = set()

            self.fishnet[data.get('name')].add(news)

            return news

    def get_message_id(self, article_number):
        """Returns the Message-ID for a article number and strips out the <>"""
        return self.connection.stat(article_number)[2][1:-1]

    def set_group(self, group_name):
        """Sets the group for this manager.

        Here we make use of namedtuple since we don't really have a
        good reason to create a separate class.
        """
        LOGGER.info('Setting group to %s', group_name)
        self.group = self.NewsGroup(*self._get_connection().group(group_name))

        LOGGER.info('Group created: %s', self.group.name)
        LOGGER.info('Count: %s', self.group.count)
        LOGGER.info('First: %s', self.group.first)
        LOGGER.info('Last: %s', self.group.last)
        self.router = RegexRouter(self.group)

    def get_headers(self, first, last):
        """Gets headers from the remote server."""
        connection = self._get_connection()

        if self.group.name is None:
            return tuple()

        xhdr_query = self._get_xhdr_string(first, last)
        LOGGER.debug('NNTP Query: %s', xhdr_query)

        headers = connection.xhdr(self.HEADER, xhdr_query)
        return headers[1]  # [0] is useless information

    def close(self):
        """Closes nntp connection."""
        try:
            self._get_connection().quit()
            LOGGER.info('Connection closed.')
        except nntplib.NNTPPermanentError:
            LOGGER.info('Connection had already timeout.')



