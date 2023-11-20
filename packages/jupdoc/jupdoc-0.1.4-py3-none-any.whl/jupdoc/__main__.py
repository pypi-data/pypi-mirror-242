"""
Entry point of the library for website backends and CLI applications.
"""
import logging

import coloredlogs

from .main import Main

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)


def main():
    main_obj = Main()
    main_obj.run()


if __name__ == "__main__":
    main()
