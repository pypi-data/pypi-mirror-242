"""
Extra functions
"""

import sys


def report(error_type):
    errors = [ValueError, RecursionError, ReferenceError, SyntaxError, SystemError, OSError, UnicodeError,
              BaseException, IOError, BlockingIOError, TabError, KeyError, KeyboardInterrupt, BrokenPipeError,
              'normal']
    if error_type in errors and error_type != 'normal':
        raise error_type
    elif error_type in errors and error_type == 'normal':
        print('ERROR 404: Option not found.')
        sys.exit(0)
    else:
        return report('normal')
