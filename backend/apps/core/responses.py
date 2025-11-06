# Python Imports
from typing import Any, Optional

# DRF Imports
from rest_framework.response import Response as DRFResponse


class Response(DRFResponse):

    _status_text = "SUCCESS"

    def __init__(
        self,
        data: Optional[Any] = None,
        status_code: Optional[int] = None,
        status_text: Optional[str, None] = None,
        template_name: Optional[str, None] = None,
        headers: Optional[dict] = None,
        content_type: Optional[str] = None,
    ):

        if status_text:
            self._status_text = status_text

        super().__init__(
            data,
            status=status_code,
            template_name=template_name,
            headers=headers,
            content_type=content_type,
        )

    @property
    def status_text(self):
        return self._status_text
