from argparse import ArgumentParser, Namespace
from ..utils.logging import setup_logger

import logging as lg
import sys
import os


class TeisatsuCLI:
    def __init__(self) -> None:
        self.argparser = ArgumentParser(
            description='will find everything',
            epilog='see wandderq/teisatsu (github)'
        )
        
        self.argparser.add_argument(
            'thing',
            help='What we\'re looking for'
        )
        self.argparser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Verbose mode, debug logs'
        )
        self.argparser.add_argument(
            '-L', '--log-file',
            default=None,
            help='Write logs to the file'
        )
        
    
    def run(self) -> None | int:
        args = self.argparser.parse_args()
        logger = setup_logger(
            lg.DEBUG if args.verbose else lg.INFO,
            args.log_file
        )
        


def run_teisatsu() -> None:
    cli = TeisatsuCLI()
    exitcode = cli.run()
    sys.exit(exitcode)