import colorlog as clg
import logging as lg
import sys


def setup_logger(level: int, file_path: str | None) -> lg.Logger:
    logger = lg.getLogger('teisatsu')
    logger.handlers.clear()
    logger.setLevel(lg.DEBUG)
    
    stream_handler = lg.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(clg.ColoredFormatter(
        fmt="[{log_color}{name} - {levelname}{reset}]: {message}",
        style='{',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red'
        }
    ))
    stream_handler.setLevel(level)
    logger.addHandler(stream_handler)
    
    if file_path:
        file_handler = lg.FileHandler(file_path, mode='a', encoding='utf-8')
        file_handler.setFormatter(lg.Formatter(
            fmt="[{asctime} - {name} - {levelname}]: {message}",
            style='{',
            datefmt="%d/%m/%Y %H:%M:%S"
        ))
        
        file_handler.setLevel(lg.DEBUG)
        logger.addHandler(file_handler)
    
    return logger