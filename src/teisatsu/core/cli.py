from argparse import ArgumentParser, Namespace
from pathlib import Path

import colorlog as clg
import logging as lg
import sys
import os


def fprint(s: str='', end: str='\n'):
    sys.stdout.write(str(s) + str(end))
    sys.stdout.flush()


def print_header(text: str) -> None:
    text = ' ' + text.strip() + ' '
    text_size = len(text)
    head_size = os.get_terminal_size().columns - text_size
    left_size = head_size // 2
    right_size = head_size - left_size
    
    fprint('-'*left_size + text + '-'*right_size)


class TeisatsuCLI:
    def __init__(self) -> None:
        self.argparser = ArgumentParser(
            description='Will find everything (almost)',
            epilog='See https://github.com/wandderq/teisatsu'
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
            help='Separator between args.things, like sep.join(thing)'
        )
        find_parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Verbose mode'
        )
        
        # list command parser
        list_parser = subparsers.add_parser('list', help='Shows available things')
        list_parser.add_argument(
            'object',
            choices=['tags', 'scripts'],
            help='Displays the available [object]'
        )

        list_parser.add_argument(
            '-m', '--more',
            action='store_true',
            help='Show more info'
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
        from ..managers.classifier import TClassifierManager
        from ..managers.script import TScriptManager
        
        thing = args.separator.join(args.thing)
        self.logger.debug(f'Got thing: {thing}')
        
        # Getting tags
        classifier_manager = TClassifierManager()
        classifier_manager.load_classifiers()
        tags = classifier_manager.classify(thing)
        
        if not tags:
            self.logger.error(f'Failed to classificate: {thing}')
            return 1
        
        # running scripts
        script_manager = TScriptManager()
        script_manager.load_scripts()
        
        if not script_manager.scripts:
            self.logger.error(f'No scripts found')
            return 1
        
        for script_name, results in script_manager.run_scripts(thing, tags):
            print_header(script_name)
            fprint('\n'.join(f"{key}: {val}" for key, val in results.items()))
            
            
    def display_available_tags(self, args: Namespace) -> None:
        from .tags import Tag

        if not args.more:
            fprint('Available tags: ', end='')
            fprint(', '.join([t.name for t in Tag]))
            fprint(f'Total: {len(Tag)}')
            return

        else:
            fprint('Available tags:')
            for tag in Tag:
                fprint(f'Name: {tag.name}, Value: {tag.value}')
            return
    
    
    def display_available_scripts(self, args: Namespace) -> None:
        from ..managers.script import TScriptManager

        script_manager = TScriptManager()
        script_manager.load_scripts()
        
        scripts = script_manager.scripts

        if not args.more:
            script_strings = [
                f"{name}[{tags}]" for name, tags in [
                    (
                        script['name'],
                        ','.join([t.name for t in script['tags']])
                    )
                    for script in scripts
                ]
            ] # tf is happening here
            
            fprint(f"Available scripts: {', '.join(script_strings)}")

        else:
            for script in scripts:
                name = script['name']
                tags = ','.join([t.name for t in script['tags']])
                version = script['version']
                description = script['desc']
                requirements = ','.join(script['requirements']) if script['requirements'] else None

                fprint(f'Name: {name}')
                fprint(f'Tags: {tags}')
                fprint(f'Version: {version}')
                fprint(f'Requirements: {requirements}')
                fprint(f'Description: {description}')
                fprint()


    def run(self) -> None | int:
        args = self.argparser.parse_args()
        
        self.setup_logger(lg.DEBUG if hasattr(args, 'verbose') and args.verbose else lg.WARNING)
        self.logger.debug(f'CLI launched. Executing command: {args.command}')
        
        if args.command == 'find':
            returncode = self.find_thing(args)
            return returncode
        
            
        elif args.command == 'list':
            self.logger.debug(f'Displaying the available {args.object}')
            if args.object == 'tags':
                self.display_available_tags(args)
                return 0
            
            if args.object == 'scripts':
                self.display_available_scripts(args)
                return 0



def launch_cli():
    exitcode = TeisatsuCLI().run()
    sys.exit(exitcode)