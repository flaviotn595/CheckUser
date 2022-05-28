import sys

import app.checker.cli as check_user_cli
import app.service.cli as service_cli
import app.web.cli as web_cli

from app.utils import base_cli


def args_handler(args):
    check_user_cli.args_handler(args)
    service_cli.args_handler(args)
    web_cli.args_handler(args)

def main():
    if len(sys.argv) == 1:
        base_cli.print_help()
        return

    args = base_cli.parse_args()
    args_handler(args)

if __name__ == '__main__':
    sys.exit(main())