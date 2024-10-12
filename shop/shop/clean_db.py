"""The script to remove database and temporary files."""
from shutil import rmtree
from os import remove
from pathlib import Path

PROJECT_DIR = Path(__file__).absolute().parent
DB_PATH = PROJECT_DIR.joinpath('db.sqlite3')
TMP_PATH = PROJECT_DIR.joinpath('tmp')

try:
    remove(DB_PATH)
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
    try:
        rmtree(migrations_path)
        print(f'"{migrations_path}" is removed.')
    except FileNotFoundError:
        print(f'"{migrations_path}" is not found.')
