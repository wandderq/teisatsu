from argparse import ArgumentParser, Namespace
from pathlib import Path

import colorlog as clg
import logging as lg
import sys
import os

def fprint(s: str='', end: str='\n'):
    sys.stdout.write(str(s) + str(end))
    sys.stdout.flush()


class TeisatsuCLI:
    def __init__(self) -> None:
        self.argparser = ArgumentParser(
            description='will find everything (almost)',
            epilog='see https://github.com/wandderq/teisatsu'
        )
        
        subparsers = self.argparser.add_subparsers(
            dest='command',
            help='teisatsu command',
            metavar='[command]',
            required=True
        )
        
        # find command parser
        find_parser = subparsers.add_parser('find', help='find anyTHING')
        find_parser.add_argument('thing', help='search request')
        find_parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='verbose mode'
        )
        
        # list command parser
        list_parser = subparsers.add_parser('list', help='shows available things')
        list_parser.add_argument(
            'object',
            choices=['tags', 'scripts'],
            help='displays the available [object]'
        )
        
    
    def __setup_logger(self, level: int) -> lg.Logger:
        self.logfile_path = Path('~/.local/tmp/teisatsu.log').expanduser()
        self.logfile_path.parent.mkdir(parents=True, exist_ok=True)
        self.logfile_path.touch(exist_ok=True)
        
        
        root_logger = lg.getLogger('teisatsu')
        root_logger.handlers.clear()
        root_logger.setLevel(lg.DEBUG)
        
        stream_handler = lg.StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(level=level)
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
        
        file_handler = lg.FileHandler(str(self.logfile_path), mode='a', encoding='utf-8')
        file_handler.setFormatter(lg.Formatter(
            fmt="[{asctime} - {levelname} - {name}]: {message}",
            style='{'
        ))
        
        root_logger.addHandler(stream_handler)
        root_logger.addHandler(file_handler)
        
        return lg.getLogger('teisatsu.cli')
    
    
    def __find_thing(self, args: Namespace) -> None | int:
        ...
    
    
    def __display_available_tags(self) -> None:
        ...
    
    
    def __display_available_scripts(self) -> None:
        ...
    
    
    def run(self) -> None | int:
        args = self.argparser.parse_args()
        logger = self.__setup_logger(lg.DEBUG if args.verbose else lg.INFO)
        
        logger.debug(f'CLI launched. Executing command: {args.command}')
        
        if args.command == 'find':
            returncode = self.__find_thing(args)
            return returncode
        
            
        elif args.command == 'list':
            logger.debug(f'Displaying the available {args.object}')
            if args.object == 'tags':
                self.__display_available_tags()
                return 0
            
            if args.object == 'scripts':
                self.__display_available_scripts()
                return 0



def launch_cli():
    exitcode = TeisatsuCLI().run() 
    sys.exit(exitcode)
