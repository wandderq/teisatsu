from argparse import ArgumentParser
# from pprint import pprint
# from ..core.classifier import TeisatsuClassifier

import colorlog as clg
import logging as lg
import json
import sys
# import os


def fprint(s: str='', end: str='\n') -> None:
    sys.stdout.write(f'{s}{end}')
    sys.stdout.flush()

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
        
        # global args
        self.argparaser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='verbose mode'
        )
    
    
    def setup_logger(self, level: int) -> lg.Logger:
        root_logger = lg.getLogger('teisatsu')
        root_logger.handlers.clear()
        root_logger.setLevel(level)
        
        stream_handler = clg.StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(clg.ColoredFormatter(
            fmt="[{name} - {log_color}{levelname}{reset}]: {message}",
            style='{',
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red'
            }
        ))
        
        root_logger.addHandler(stream_handler)
        
        return lg.getLogger('teisatsu.cli')
        
    
    def show_tags(self) -> None:
        from ..core.groups import TAGS
        fprint(f'Availavble tags: {len(TAGS)}')
        show = not (input('show? y/n: ').strip().lower() in ['n', 'no'])
        
        if show:
            fprint()
            for i, tag in enumerate([t['name'] for t in TAGS], start=1):
                fprint(f'{i}: {tag}')
        
    
    def run(self) -> None | int:
        args = self.argparaser.parse_args()
        logger = self.setup_logger(lg.DEBUG if args.verbose else lg.INFO)
        
        if args.command == 'find':
            from ..core.classifier import TeisatsuClassifier
            from ..core.manager import TeisatsuScriptManager
            
            # parsing thing
            thing = str(args.thing).strip()
            logger.debug(f'Thing: {thing}')
            
            
            # classifying
            logger.info('Classifying thing')
            classifier = TeisatsuClassifier(thing)
            tags = classifier.classify()
            if not tags: return 1
            logger.debug(f'Classified tags: {tags}')
            
            
            # gathering scripts
            logger.info('Getting scripts')
            manager = TeisatsuScriptManager()
            scripts = manager.get_scripts(tags)
            if not scripts: return 1
            logger.debug(f'Match scripts: {[s['name'] for s in scripts]}')
            
            
            # running scripts (gathering information)
            logger.info('Running scripts')
            raw_info = manager.run_scripts(thing, scripts)
            
            print(json.dumps(
                raw_info,
                ensure_ascii=False,
                indent=4
            ), flush=True)
            
            # summaring information
            ...
            
            
            # showing & saving results
            ...
            
        
        
        elif args.command == 'list':
            if args.object == 'tags':
                self.show_tags()
            
            if args.object == 'scripts':
                ...



def launch_cli() -> None:
    cli = TeisatsuCLI()
    exitcode = cli.run()
    sys.exit(0 if not exitcode else exitcode)