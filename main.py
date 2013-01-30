#!/usr/bin/env python
"""
Indexes nzbs.
"""
__author__ = 'cozzi.martin@gmail.com'


import argparse
import logging
import nntplib


def main():
    """Entry point"""
    configs = get_configs()


def get_configs():
    """Get configs from argparse"""
    parser = argparse.ArgumentParser(
        description='Small client that connects to a newsgroup server')
    parser.add_argument('--nzb_host', type=str, required=True,
                        help='Newsgroup server url')
    args = parser.parse_args()
    return args


def get_logger():
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
