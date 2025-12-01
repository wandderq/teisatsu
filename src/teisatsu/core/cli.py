from argparse import ArgumentParser
from ..core.classifier import TeisatsuClassifier

import sys
import os



class TeisatsuCLI:
    def __init__(self) -> None:
        self.argparaser = ArgumentParser(
            description='will find everything',
            epilog='see wandderq/teisatsu (github)'
        )
        
        subparsers = self.argparaser.add_subparsers(
            dest='command',
            help='teisatsu command',
            metavar='[command]',
            required=True
        )
        
        # find command parser
        find_parser = subparsers.add_parser(
            'find',
            help='find anyTHING'
        )
        
        find_parser.add_argument(
            'thing',
            help='what we\'re searching about'
        )
        
        # list command parser
        list_parser = subparsers.add_parser(
            'list',
            help='shows available things'
        )
        
        list_parser.add_argument(
            'object',
            choices=['tags', 'scripts'],
            help='shows available [object]'
        )
        
    
    def run(self) -> None | int:
        args = self.argparaser.parse_args()
        
        if args.command == 'find':
            thing = str(args.thing).strip()
            
            classifier = TeisatsuClassifier(thing)
            tags = classifier.classify()
        
        
        elif args.command == 'list':
            ...



def launch_cli() -> None:
    cli = TeisatsuCLI()
    exitcode = cli.run()
    sys.exit(0 if not exitcode else exitcode)