"""
Rename the project everywhere except third-party code.

Usage
-----
    uv run rename_project.py new

The script preserves casing:
  old  -> new
  Old  -> New
  OLD  -> NEW
  old_password -> new_password

"""

import argparse
import logging
import re
import shutil
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from core.project_meta import PROJECT_DISPLAY, PROJECT_NAME, PROJECT_TITLE

logger = logging.getLogger('rename_project')

excluded_dirs = {
    '.git',
    '.venv',
    'venv',
    '__pycache__',
    '.idea',
    '.pytest_cache',
    '.ruff_cache',
    'node_modules',
    'staticfiles',
    'coverage',
}
excluded_files = {
    'uv.lock',
    'db.sqlite3',
    'rename_project.py',
    '.dockerignore',
    '.gitignore',
}
included_suffixes = {
    '.py',
    '.toml',
    '.md',
    '.txt',
    '.yml',
    '.yaml',
    '.json',
    '.html',
    '.css',
    '.js',
    '.ini',
    '.cfg',
    '.env',
    '',
}
included_stems = {
    'Dockerfile',
}
protected_line_prefixes = (
    'POSTGRES_DB',
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'DJANGO_SECRET_KEY',
    'test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER',
)
ROOT = Path.cwd()


@dataclass(frozen=True)
class Replacement:
    """A single compiled substitution rule."""

    pattern: re.Pattern[str]
    replacement: str

    def apply(self, text: str) -> tuple[str, int]:
        """Apply the substitution rule."""
        return self.pattern.subn(
            repl=self.replacement,
            string=text,
        )


@dataclass(frozen=True)
class RenameResult:
    """A single rename result."""

    file_changes: list[tuple[Path, int]]
    dir_renames: list[tuple[Path, Path]]


def parse() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Rename the project.')
    parser.add_argument(
        'new_name',
        help='New project name in lower case.',
    )
    return parser.parse_args()


def validate(new: str) -> str | None:
    """Return an error message, or None if arguments are valid."""
    if new == PROJECT_NAME:
        return f'Old and new names are identical: {PROJECT_NAME}'
    if not re.fullmatch(r'[a-z][a-z0-9_]*', new):
        return f'New name must match [a-z][a-z0-9_]*: {new}'
    return None


def get_file_changes(new: str) -> list[tuple[Path, int]]:
    """Rename the project."""
    replacements = build_replacements(new=new)

    file_changes: list[tuple[Path, int]] = []
    for path in iter_files():
        count = rewrite_file(
            path=path,
            replacements=replacements,
        )
        if count:
            file_changes.append((path, count))
            logger.info('  edit  %s (%d replacements)', path, count)
    return file_changes


def rename_directories(
    dirs: list[Path],
    new: str,
) -> list[tuple[Path, Path]]:
    """Rename the directories."""
    renames: list[tuple[Path, Path]] = []
    pattern = re.compile(
        pattern=re.escape(PROJECT_NAME),
        flags=re.IGNORECASE,
    )

    for directory in dirs:
        if PROJECT_NAME not in directory.name.lower():
            continue
        new_name = pattern.sub(repl=new, string=directory.name)
        target = directory.with_name(name=new_name)
        renames.append((directory, target))
        shutil.move(src=str(directory), dst=str(target))

    return renames


def build_replacements(new: str) -> tuple[Replacement, ...]:
    """Build replacement tuple."""
    variants = (
        (PROJECT_NAME.lower(), new.lower()),
        (PROJECT_TITLE, new.capitalize()),
        (PROJECT_DISPLAY, new.upper()),
    )
    return tuple(
        Replacement(
            pattern=re.compile(re.escape(src)),
            replacement=dst,
        )
        for src, dst in variants
    )


def iter_files() -> Iterable[Path]:
    """Iterate over all files in this project."""
    for path in ROOT.rglob('*'):
        if any(part in excluded_dirs for part in path.parts):
            continue
        if path.is_file() and is_file_processed(path):
            yield path


def rewrite_file(
    path: Path,
    replacements: tuple[Replacement, ...],
) -> int:
    """
    Apply replacements to *path*, skipping protected lines.

    Returns
    -------
    int
        Total number of substitutions performed (0 means file unchanged).

    """
    try:
        original = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return 0

    new_lines: list[str] = []
    total = 0

    for line in original.splitlines(keepends=True):
        if is_line_protected(line):
            new_lines.append(line)
            continue

        updated = line
        for rule in replacements:
            updated, count = rule.apply(updated)
            total += count
        new_lines.append(updated)

    if total:
        path.write_text(''.join(new_lines), encoding='utf-8')
    return total


def is_file_processed(path: Path) -> bool:
    """Whether the given path is a file processed or not."""
    if path.name in excluded_files:
        return False
    if path.name in included_stems:
        return True
    return path.suffix.lower() in included_suffixes


def is_line_protected(line: str) -> bool:
    """Whether the given line is a protected line."""
    stripped = line.lstrip().removeprefix('export ').lstrip()
    return any(
        stripped.startswith((f'{key}=', f'{key}:', f'"{key}"'))
        for key in protected_line_prefixes
    )


def iter_dirs() -> list[Path]:
    """Return all non-excluded directories, deepest first."""
    return sorted(
        (
            path for path in ROOT.rglob('*')
            if path.is_dir()
            and not any(part in excluded_dirs for part in path.parts)
        ),
        key=lambda path: len(path.parts),
        reverse=True,
    )


def rename_project(new: str) -> RenameResult:
    """Rename the project."""
    file_changes = get_file_changes(new=new)
    dir_renames = rename_directories(
        dirs=iter_dirs(),
        new=new,
    )
    for src, dst in dir_renames:
        logger.info('  move  %s -> %s', src, dst)

    return RenameResult(file_changes=file_changes, dir_renames=dir_renames)


def main() -> int:
    """Run the renaming script."""
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    new = parse().new_name.lower()
    error = validate(new)
    if error:
        logger.error(error)
        return 1

    logger.info('%s -> %s', PROJECT_NAME, new)
    rename_result = rename_project(new=new)

    logger.info(
        'Summary: %d files updated, %d directories renamed.',
        len(rename_result.file_changes),
        len(rename_result.dir_renames),
    )
    subprocess.run(
        ['uv', 'lock'],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())
