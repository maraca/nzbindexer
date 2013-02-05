#!/usr/bin/env python
"""
Indexes nzbs.
"""
__author__ = 'cozzi.martin@gmail.com'


import argparse
import getpass
import logging
import nntplib


from collections import namedtuple


class NZBManager:
    """Manages connections and tasks and such."""

    def __init__(self, configs):
        """Inits itself."""
        self.configs = configs
        self.connection = None
        self.group = None

    def _connect(self):
        """Connects to a remote Usenet server"""
        LOGGER.info('New remote connection')
        connection = nntplib.NNTP(
                self.configs.nzb_host,
                user=self.configs.nzb_user,
                password=self.configs.nzb_password)
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
                self.configs.nzb_host, self.configs.nzb_user)
        LOGGER.info('Server says: "%s"', self.connection.getwelcome())

        return self.connection

    def set_group(self, group_name):
        """Sets the group for this manager.

        Here we make use of namedtuple since we don't really have a
        good reason to create a separate class.
        """
        LOGGER.info('Setting group to %s', group_name)
        NZBGroup = namedtuple('NZBGroup',
                ['response', 'count', 'first', 'last', 'name'])
        self.group = NZBGroup(*self._get_connection().group(group_name))

        LOGGER.info('Group created: %s', self.group.name)
        LOGGER.info('Count: %s', self.group.count)
        LOGGER.info('First: %s', self.group.first)
        LOGGER.info('Last: %s', self.group.last)


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
    manager = NZBManager(configs)
    manager.set_group(configs.nzb_group)
    manager.close()


def get_configs():
    """Get configs from argparse"""
    parser = argparse.ArgumentParser(
        description='Small client that connects to a newsgroup server')
    parser.add_argument('--nzb_host', type=str, required=True,
                        help='Newsgroup server url')
    parser.add_argument('--nzb_user', type=str, required=True,
                        help='Newsgroup username')
    parser.add_argument('--nzb_password', type=str,
                        help='Newsgroup password')
    parser.add_argument('--nzb_group', type=str,
                        help='Newsgroup group to parse')
    args = parser.parse_args()
    if not args.nzb_password:
        args.nzb_password = getpass.getpass('Newsgroup password: ')
    return args


def get_logger():
    """Builds up a basic python logger."""
    logger = logging.getLogger('nzbindexer')
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
