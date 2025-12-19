# Python Imports
from typing import Optional


def before_send_filter(event: dict, hint: dict) -> Optional[dict]:
    """Filter event before send it to Sentry"""
    if (
        event.get("logger") == "django.request"
        and event.get("django.request")
        and event.get("level") == "error"
    ):
        if "404" in str(hint.get("exc_info", "")):
            return None

    return event


def before_breadcrumb_filter(crumb: dict, hint: dict) -> Optional[dict]:
    """Filter breadcrumb before send it to Sentry"""

    # Prevent log exernal API calls with query params holding tokens
    if crumb.get("category") == "httplib" and "token=" in crumb.get("data", {}).get("url", ""):
        return None

    return crumb
