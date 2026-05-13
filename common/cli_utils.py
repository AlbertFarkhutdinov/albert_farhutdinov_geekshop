"""The module provides command-line interface (CLI) utils."""

from argparse import ArgumentParser, Namespace

DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 8000


def get_args() -> Namespace:
    """
    Return command-line arguments parsed from ``sys.argv``.

    Returns
    -------
    argparse.Namespace
        Parsed arguments with the following attribute:

        ``host`` : str, default: DEFAULT_HOST
            API host.
        ``port`` : int, default: DEFAULT_PORT
            API port.

    """
    parser = ArgumentParser()
    parser.add_argument(
        '--host',
        default=DEFAULT_HOST,
        help='API host',
    )
    parser.add_argument(
        '--port',
        default=DEFAULT_PORT,
        type=int,
        help='API port',
    )
    return parser.parse_args()
