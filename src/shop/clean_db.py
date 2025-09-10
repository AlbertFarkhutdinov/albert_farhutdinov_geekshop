"""The script to remove database and temporary files."""
from pathlib import Path
from shutil import rmtree

PROJECT_DIR = Path(__file__).absolute().parent
DB_PATH = PROJECT_DIR.joinpath('db.sqlite3')
TMP_PATH = PROJECT_DIR.joinpath('tmp')

try:
    DB_PATH.unlink()
except FileNotFoundError:
    print('"{0}" is not found.'.format(DB_PATH))
else:
    print('"{0}" is removed.'.format(DB_PATH))

try:
    rmtree(TMP_PATH)
except FileNotFoundError:
    print('"{0}" is not found.'.format(TMP_PATH))
else:
    print('"{0}" is removed.'.format(TMP_PATH))

APPS = (
    'admin_app',
    'auth_app',
    'basket_app',
    'main_app',
    'orders_app',
)
for app in APPS:
    migrations_path = PROJECT_DIR.joinpath(app, 'migrations')
    if migrations_path.exists():
        for path in migrations_path.iterdir():
            if path.name != '__init__.py':
                if path.is_file():
                    path.unlink()
                else:
                    rmtree(path)
        print('Migrations from "{0}" are removed.'.format(migrations_path))
    else:
        print('"{0}" is not found.'.format(migrations_path))
