import argparse

from app import __version__

base_cli = argparse.ArgumentParser(description='Check user', prog='check_user v%s' % __version__)
base_cli.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s',
)
