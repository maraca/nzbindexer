#!/usr/bin/env python
"""
Pulls data from Usenet and indexes it *somewhere*.
"""
__author__ = 'cozzi.martin@gmail.com'


import argparse
import getpass
import logging

from collections import namedtuple
from usenet import UsenetManager


def main():
    """Entry point"""
    configs = get_configs()
    manager = UsenetManager(configs)
    manager.set_group(configs.usenet_group)

    headers = manager.get_headers(int(manager.group.last) - configs.pagination,
                                  manager.group.last)
    for header in headers[1]:
        manager.get_info(header)

    print(manager.fishnet)
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
