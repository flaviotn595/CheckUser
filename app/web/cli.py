from ..utils import base_cli, logger, Config
from ..web import ServerManager

base_cli.add_argument(
    '--start-server',
    action='store_true',
    help='Start server',
)

base_cli.add_argument(
    '--server-host',
    default='0.0.0.0',
    help='Server host',
)

base_cli.add_argument(
    '--server-port',
    type=int,
    help='Server port',
)

base_cli.add_argument(
    '--server-num-workers',
    default=3,
    type=int,
    help='Server number of workers',
)

base_cli.add_argument(
    '--server-use-thread',
    action='store_true',
    help='Server use thread',
)


def args_handler(args):
    if args.start_server:
        if args.server_port is None:
            args.server_port = Config().port

        server = ServerManager(
            args.server_host,
            args.server_port,
            args.server_num_workers,
            args.server_use_thread,
        )
        server.start()
