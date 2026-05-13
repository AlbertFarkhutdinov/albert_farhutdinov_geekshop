"""Template context processors exposing project-wide metadata."""

from django.http import HttpRequest

from core.project_meta import (
    PROJECT_DESCRIPTION,
    PROJECT_DISPLAY,
    PROJECT_NAME,
    PROJECT_TITLE,
)


def project_meta(request: HttpRequest) -> dict[str, str]:
    """
    Expose project naming constants to every template.

    Parameters
    ----------
    request : HttpRequest
        The current request (unused, but required by Django).

    Returns
    -------
    dict[str, str]
        Mapping of template variables to their values.

    """
    return {
        'project_name': PROJECT_NAME,
        'project_title': PROJECT_TITLE,
        'project_display': PROJECT_DISPLAY,
        'project_description': PROJECT_DESCRIPTION,
    }
