from app.checker import check_user, kill_user
from app.checker import CheckerUserManager

from app.checker.ovpn import OpenVPNManager
from app.checker.ssh import SSHManager

from app.web import Server, ServerManager

from app.utils import base_cli

__version__ = '2.1.1'
__author__ = 'Glemison C. Dutra'
__email__ = 'glemyson20@gmail.com'

base_cli.description = 'Checker for OpenVPN and SSH'
base_cli.prog = 'checker v' + __version__

base_cli.add_argument(
    '-v',
    '--version',
    action='version',
    version='%(prog)s',
)
