from argparse import ArgumentParser, Namespace
from pathlib import Path

import colorlog as clg
import logging as lg
import json
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
        find_parser.add_argument('thing', help='search request', nargs='+', type=str)
        find_parser.add_argument(
            '-s', '--separator',
            type=str,
            default=' ',
            help='separator between args.things, like sep.join(thing)'
        )
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
    
    
    def setup_logger(self, level: int) -> None:
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
        
        self.logger = lg.getLogger('teisatsu.cli')
    
    
    def find_thing(self, args: Namespace) -> None | int:
        from .plugins import TPluginManager, TClassifierManager, TScriptManager
        from .data import TDataProcessor
        
        thing = args.separator.join(args.thing)
        self.logger.debug(f'Got thing: {thing}')
        
        plugin_manager = TPluginManager()
        plugins = plugin_manager.discover_plugins()
        
        if not plugins:
            self.logger.error(f'No plugins found')
            return 1
        
        classifier_manager = TClassifierManager(plugins['classifiers'])
        tags = classifier_manager.classify(thing)
        
        if not tags:
            self.logger.error(f'Failed to classificate: {thing}')
            return 1
        
        script_manager = TScriptManager(plugins['scripts'])
        data_processor = TDataProcessor()
        
        for script in script_manager.iter_scripts(tags):
            raw_data = script_manager.run_script(script, thing)
            data = data_processor.process(raw_data)
            fprint(json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            ))
            
            
    def __display_available_tags(self) -> None:
        ...
    
    
    def __display_available_scripts(self) -> None:
        ...
    
    
    def run(self) -> None | int:
        args = self.argparser.parse_args()
        
        self.setup_logger(lg.DEBUG if hasattr(args, 'verbose') and args.verbose else lg.INFO)
        self.logger.debug(f'CLI launched. Executing command: {args.command}')
        
        if args.command == 'find':
            returncode = self.find_thing(args)
            return returncode
        
            
        elif args.command == 'list':
            self.logger.debug(f'Displaying the available {args.object}')
            if args.object == 'tags':
                self.__display_available_tags()
                return 0
            
            if args.object == 'scripts':
                self.__display_available_scripts()
                return 0



def launch_cli():
    exitcode = TeisatsuCLI().run() 
    sys.exit(exitcode)
