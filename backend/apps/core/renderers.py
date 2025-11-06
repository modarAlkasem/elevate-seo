# Python Imports
from typing import Any, Optional

# REST Framework Imports
from rest_framework.renderers import JSONRenderer as DRFJSONRenderer

# App Imports
from .responses import Response


class JSONRenderer(DRFJSONRenderer):

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[dict] = None,
    ) -> bytes:
        response: Response = renderer_context.get("response")
        status_code = response.status_code
        status_text = response.status_text
        wrapped_data = {"status_code": status_code}

        if status_code >= 400:
            wrapped_data["errors"] = data
        else:
            wrapped_data["data"] = data

        if status_text == "SUCCESS" and status_code >= 500:
            status_text = "UNKNOWN_ERROR"
        elif status_text == "SUCCESS" and status_code >= 400:
            status_text = "BAD_REQUEST"

        wrapped_data["status_text"] = status_text

        return super().render(wrapped_data, accepted_media_type, renderer_context)
