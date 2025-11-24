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
            nargs='+',
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
            metavar='PATH',
            help='Write logs to the file'
        )
        
        self.argparser.add_argument(
            '-j', '--join',
            default=' ',
            type=str,
            help='separator between things (default: space)'
        )
        
    
    def run(self) -> None | int:
        args = self.argparser.parse_args()
        thing = str(args.join).join(args.thing)
        
        setup_logger(lg.DEBUG if args.verbose else lg.INFO, args.log_file)
        logger = lg.getLogger('teisatsu.cli')
        logger.info(f'Got thing: {thing}')
        
        
        # Getting thing's tags
        from ..core.bunruki import BunrukiClassifier
        classifier = BunrukiClassifier(thing)
        tags = classifier.classify(raise_exception=True)

        if not tags:
            return 1
        
        
        # WIP
        


def run_teisatsu() -> None:
    cli = TeisatsuCLI()
    exitcode = cli.run()
    sys.exit(exitcode)