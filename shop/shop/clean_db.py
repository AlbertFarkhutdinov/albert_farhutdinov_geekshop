"""The script to remove database and temporary files."""
from shutil import rmtree
from pathlib import Path

PROJECT_DIR = Path(__file__).absolute().parent
DB_PATH = PROJECT_DIR.joinpath('db.sqlite3')
TMP_PATH = PROJECT_DIR.joinpath('tmp')

try:
    DB_PATH.unlink()
    print(f'"{DB_PATH}" is removed.')
except FileNotFoundError:
    print(f'"{DB_PATH}" is not found.')

try:
    rmtree(TMP_PATH)
    print(f'"{TMP_PATH}" is removed.')
except FileNotFoundError:
    print(f'"{TMP_PATH}" is not found.')

for app in (
    'admin_app',
    'auth_app',
    'basket_app',
    'main_app',
    'orders_app',
):
    migrations_path = PROJECT_DIR.joinpath(app, 'migrations')
    if migrations_path.exists():
        for path in migrations_path.iterdir():
            if path.name != '__init__.py':
                if path.is_file():
                    path.unlink()
                else:
                    rmtree(path)
        print(f'Migrations from "{migrations_path}" are removed.')
    else:
        print(f'"{migrations_path}" is not found.')
