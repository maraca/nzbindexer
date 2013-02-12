#!/usr/bin/env python
"""
Pulls data from Usenet and indexes it *somewhere*.
"""
__author__ = 'cozzi.martin@gmail.com'


import argparse
import getpass
import logging
import yaml

from collections import namedtuple
from indexer import NewsGroupIndexer
from usenet import UsenetManager


def main():
    """Entry point"""
    configs = get_configs()
    configs = configs.configs
    group = configs['usenet']['groups'][0]
    manager = UsenetManager(configs)
    manager.set_group(group)

    indexer = NewsGroupIndexer(configs['cassandra'])

    start = int(manager.group.last) - configs['usenet']['pagination']
    last =  int(manager.group.last)
    headers = manager.get_headers(start, last)

    for header in headers:
        data = manager.get_header_data(header)
        indexer.add_segment(data.subject, data.segment, data.message_id, group)

    manager.close()


def get_configs():
    """Get configs from argparse"""
    parser = argparse.ArgumentParser(
        description='Small client that connects to a newsgroup server')
    parser.add_argument('--config-file', type=str, required=True,
                        help='Path to configs.yaml')
    args = parser.parse_args()
    with open(args.config_file) as configurations:
        args.configs = yaml.load(configurations)

    if not args.configs['usenet'].get('password'):
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
