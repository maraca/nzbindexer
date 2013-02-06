#!/usr/bin/env python
"""
Pulls data from Usenet and indexes it *somewhere*.
"""
__author__ = 'cozzi.martin@gmail.com'


import argparse
import getpass
import logging
import nntplib


from collections import namedtuple


class UsenetManager:
    """Manages connections and tasks and such."""

    NewsGroup = namedtuple('NewsGroup',
            ['response', 'count', 'first', 'last', 'name'])

    HEADER = 'Subject'

    def __init__(self, configs):
        """Inits itself."""
        self.configs = configs
        self.connection = None
        self.group = self.NewsGroup(*(None, ) * 5)

    def _connect(self):
        """Connects to a remote Usenet server"""
        LOGGER.info('New remote connection')
        connection = nntplib.NNTP(
                self.configs.usenet_host,
                user=self.configs.usenet_user,
                password=self.configs.usenet_password)
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
                self.configs.usenet_host, self.configs.usenet_user)
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

    def get_headers(self, first, last):
        """Gets headers from the remote server."""
        connection = self._get_connection()

        if self.group.name is None:
            return tuple()

        xhdr_query = self._get_xhdr_string(first, last)
        LOGGER.debug('NNTP Query: %s', xhdr_query)

        headers = connection.xhdr(self.HEADER, xhdr_query)
        return headers


    def close(self):
        """Closes nntp connection."""
        try:
            self._get_connection().quit()
            LOGGER.info('Connection closed.')
        except nntplib.NNTPPermanentError:
            LOGGER.info('Connection had already timeout.')


def main():
    """Entry point"""
    configs = get_configs()
    manager = UsenetManager(configs)
    manager.set_group(configs.usenet_group)

    headers = manager.get_headers(int(manager.group.last) - configs.pagination,
                                  manager.group.last)
    for header in headers[1]:
        print(header)
    manager.close()


def get_configs():
    """Get configs from argparse"""
    parser = argparse.ArgumentParser(
        description='Small client that connects to a newsgroup server')
    parser.add_argument('--usenet-host', type=str, required=True,
                        help='Usenet provider server url')
    parser.add_argument('--usenet-user', type=str, required=True,
                        help='Usenet provider username')
    parser.add_argument('--usenet-password', type=str,
                        help='Usenet provider password')
    parser.add_argument('--usenet-group', type=str, required=True,
                        help='Usenet group to parse')
    parser.add_argument('--pagination', type=int, default=100,
                        help='Pagination size')
    args = parser.parse_args()
    if not args.usenet_password:
        args.usenet_password = getpass.getpass('Usenet password: ')
    return args


def get_logger():
    """Builds up a basic python logger."""
    logger = logging.getLogger('usenet_indexer')
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(
        logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))

    logger.addHandler(console)
    return logger


LOGGER = get_logger()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        LOGGER.info('Caught Ctrl+C... exiting')
