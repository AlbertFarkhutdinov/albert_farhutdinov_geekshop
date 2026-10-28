"""The entrypoint for the service."""

import logging
import subprocess
import sys

import uvicorn

from common.cli_utils import get_args
from common.logging_utils import logging_uvicorn_config, set_logging_config

set_logging_config()
logger = logging.getLogger(__name__)


def run_django_command(cmd: list[str]) -> str:
    """Run a django command as a subprocess."""
    subprocess_result = subprocess.run(
        ['uv', 'run', 'manage.py', *cmd],
        capture_output=True,
        text=True,
        check=False,
    )
    if subprocess_result.returncode != 0:
        logger.error(subprocess_result.stderr)
        sys.exit(subprocess_result.returncode)
    return subprocess_result.stdout


def prepare_service() -> None:
    """Prepare the service: static files, DB migrations, etc."""
    logger.info('Collecting static files...')
    run_django_command(['collectstatic', '--noinput'])

    logger.info('Running database migrations...')
    run_django_command(['migrate', '--noinput'])

    logger.info('Starting application server...')


if __name__ == '__main__':
    args = get_args()
    logger.info(args)
    prepare_service()
    uvicorn.run(
        app='core.asgi:application',
        host=args.host,
        port=args.port,
        log_config=logging_uvicorn_config,
    )
