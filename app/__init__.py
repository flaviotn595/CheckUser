import argparse

from app.checker import check_user, kill_user
from app.checker import CheckerUserManager

from app.checker.ovpn import OpenVPNManager
from app.checker.ssh import SSHManager

from app.web import Server, ServerManager

__version__ = '2.1.1'
__author__ = 'Glemison C. Dutra'
__email__ = 'glemyson20@gmail.com'

arg_parser = argparse.ArgumentParser(description='Check user', prog='check_user v%s' % __version__)
arg_parser.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s',
)
