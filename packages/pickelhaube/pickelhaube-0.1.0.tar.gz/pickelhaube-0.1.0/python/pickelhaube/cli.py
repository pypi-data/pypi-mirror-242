#!/usr/bin/env python3
'''Main Entrypoint Module
'''
import typing
import argparse
import logging
from textwrap import dedent
import sys
from importlib.metadata import version as metadata_version


# Automatic Tab Completion
# Production Wrapper (keep the API)
class shtab:
    # Global Markers
    FILE = None
    DIRECTORY = None

    # API
    def add_argument_to(*args: typing.Any, **kwargs: typing.Any):
        pass


if __debug__:
    # Try to import the real deal
    try:
        import shtab  # type: ignore[no-redef,import-not-found] # noqa: F811
    except ImportError:
        pass


# Workaround for https://github.com/python/cpython/issues/101640
if sys.version_info >= (3, 12):
    ArgumentParser = argparse.ArgumentParser
else:
    class ArgumentParser(argparse.ArgumentParser):
        '''Wrapper for `ArgumentParser <argparse.ArgumentParser>`.

        Fixes CPython issue `#101640
        <https://github.com/python/cpython/issues/101640>`__.
        '''
        def _print_message(self, message, file=None):
            if file is None:
                pass  # Don't print if the file is unavailable
            else:
                super()._print_message(message, file=file)


# Make sure BooleanOptionalAction is available
if sys.version_info >= (3, 9):
    BooleanOptionalAction = argparse.BooleanOptionalAction
else:
    # Port from Python 3.11: https://github.com/python/cpython/blob/3.11/Lib/argparse.py#L885-L921
    class BooleanOptionalAction(argparse.Action):
        '''Port `BooleanOptionalAction
        <https://docs.python.org/3.11/library/argparse.html#action>`__ from
        Python 3.11.
        '''
        def __init__(self,
                     option_strings,
                     dest,
                     default=None,
                     required=False,
                     help=None,
                     ):

            _option_strings = []
            for option_string in option_strings:
                _option_strings.append(option_string)
                if option_string.startswith('--'):
                    option_string = '--no-' + option_string[2:]
                    _option_strings.append(option_string)

            super().__init__(
                option_strings=_option_strings,
                dest=dest,
                nargs=0,
                default=default,
                type=type,
                required=required,
                help=help,
            )

        def __call__(self, parser, namespace, values, option_string=None):
            if option_string in self.option_strings:
                setattr(namespace, self.dest, not option_string.startswith('--no-'))

        def format_usage(self):
            return ' | '.join(self.option_strings)


logger = logging.getLogger(__name__)


def main(PROJECT_NAME, PROJECT_VERSION,
         ):
    '''
    Main entrypoint to be configured
    '''
    parser = ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=dedent('''
        Prints Hello World
        '''),
        epilog=dedent(f'''
        Version {PROJECT_VERSION}
        '''),
    )
    # Automatic Tab Completion
    # - Mark certain arguments with:
    #   - `parser.add_argument(...).complete = shtab.FILE`: Complete file names
    #   - `parser.add_argument(...).complete = shtab.DIRECTORY`: Complete directory names
    shtab.add_argument_to(parser, '--generate-shtab-completion', help=argparse.SUPPRESS)

    parser.add_argument('--version', action='version', version=PROJECT_VERSION)
    parser.add_argument('-v', '--verbose', dest='loglevel',
                        action='store_const', const=logging.DEBUG, default=logging.INFO,
                        help='Add more details to the standard error log')

    args = parser.parse_args()

    # Logs
    logs_fmt = '%(levelname)-5.5s %(name)s@%(funcName)s %(message)s'
    try:
        import coloredlogs  # type: ignore
        coloredlogs.install(level=args.loglevel, fmt=logs_fmt)
    except ImportError:
        logging.basicConfig(level=args.loglevel, format=logs_fmt)
    logging.captureWarnings(True)

    print('Implement a CLI interface')

    return 0


# Release Process
def entrypoint():
    '''
    Entrypoint for executable
    '''
    __project_name__ = __package__
    __version__ = metadata_version(__project_name__)
    return main(
        PROJECT_NAME=__project_name__,
        PROJECT_VERSION=__version__,
    )


if __name__ == "__main__":
    sys.exit(entrypoint())
