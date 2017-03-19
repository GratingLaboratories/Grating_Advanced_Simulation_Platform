"""
==============================================
   __  __   __   _     .   ___            __
  / / / /  /  _ |_)   /_\   |   |  |\ |  /  _
 / / / /   \__| | \  /   \  |   |  | \|  \__|
/_/ /_/    L  A  B  O  R  A  T  O  R  I  E  S
==============================================
"""

from colorama import *
import logging
import sys
import os
import datetime

def init_all(level=logging.INFO):
    if not os.path.exists('log'):
        os.mkdir('log')

    rootLogger = logging.getLogger()
    rootLogger.setLevel(level)

    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] %(threadName)s: %(message)s")
    # fileHandler = logging.FileHandler(os.path.join('log', str(datetime.datetime.now()).replace(':', '_') + '.log'))
    # fileHandler.setFormatter(logFormatter)
    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    consoleHandler.setFormatter(Log_Formatter())
    rootLogger.addHandler(consoleHandler)
    # rootLogger.addHandler(fileHandler)


class Log_Formatter(logging.Formatter):
    def __init__(self, style='{'):
        logging.Formatter.__init__(self, style=style)

    def format(self, record):
        stdout_template = '{levelname}' + Fore.RESET + '] {threadName}: ' + '{message}'
        stdout_head = '[%s'

        allFormats = {
            logging.DEBUG: logging.StrFormatStyle(stdout_head % Fore.LIGHTBLUE_EX + stdout_template),
            logging.INFO: logging.StrFormatStyle(stdout_head % Fore.GREEN + stdout_template),
            logging.WARNING: logging.StrFormatStyle(stdout_head % Fore.LIGHTYELLOW_EX + stdout_template),
            logging.ERROR: logging.StrFormatStyle(stdout_head % Fore.LIGHTRED_EX + stdout_template),
            logging.CRITICAL: logging.StrFormatStyle(stdout_head % Fore.RED + stdout_template)
        }

        self._style = allFormats.get(record.levelno, logging.StrFormatStyle(logging._STYLES['{'][1]))
        self._fmt = self._style._fmt
        result = logging.Formatter.format(self, record)

        return result
