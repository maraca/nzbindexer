#!/usr/bin/env python
"""
Indexes nzbs.
"""
__author__ = 'cozzi.martin@gmail.com'


import argparse
import getpass
import logging
import nntplib


class NZBManager:
    """Manages connections and tasks and such."""

    def __init__(self, configs):
        """Inits itself."""
        self.configs = configs
        self.connection = self._get_connection()
        self.count = None
        self.first = None
        self.last = None
        self.name = None

    def _get_connection(self):
        """Connects to a remote Usenet server"""
        connection = nntplib.NNTP(
                self.configs.nzb_host,
                user=self.configs.nzb_user,
                password=self.configs.nzb_password)
        LOGGER.info('Connected to %s as %s',
                self.configs.nzb_host, self.configs.nzb_user)
        LOGGER.info('Server says: "%s"', connection.getwelcome())
        return connection

    def set_group(self, group_name):
        """Sets the group for this manager."""
        LOGGER.info('Setting group to %s', group_name)
        _, self.count, self.first, self.last, self.name = \
                self.connection.group(group_name)

    def close(self):
        """Closes nntp connection."""
        try:
            self.connection.quit()
            LOGGER.info('Connection closed.')
        except nntplib.NNTPPermanentError:
            LOGGER.info('Connection had already timeout.')


def main():
    """Entry point"""
    configs = get_configs()
    manager = NZBManager(configs)
    manager.set_group('alt.binaries.tv')
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
