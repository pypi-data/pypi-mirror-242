import logging

import coloredlogs

from . import convert

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)


class Main:
    def __init__(self):
        self.args = convert.parse()
        # convert.main(args)

    def run(self):
        logger.info("========= Starting conversion using jupdoc CLI =========")
        convert.main(self.args)
        logger.info("========= Finished conversion using jupdoc CLI =========")
