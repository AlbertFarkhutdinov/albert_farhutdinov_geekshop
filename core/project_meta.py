"""
Centralised project identity used across the codebase.

This module is intentionally framework-agnostic so that it can be imported
before Django is bootstrapped (``manage.py``, ``wsgi.py``, ``asgi.py``)
and from non-Django scripts.
"""

PROJECT_NAME: str = 'shop'  # lower-case slug (DB, packages, Docker)
PROJECT_TITLE: str = 'Shop'  # human-readable title (UI titles)
PROJECT_DISPLAY: str = 'SHOP'  # display/logo variant
PROJECT_DESCRIPTION: str = ""
