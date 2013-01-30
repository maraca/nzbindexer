#!/usr/bin/env python
"""
Indexes nzbs.
"""
__author__ = 'cozzi.martin@gmail.com'


import logging
import nntplib


def main():
    """Entry point"""
    pass


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
