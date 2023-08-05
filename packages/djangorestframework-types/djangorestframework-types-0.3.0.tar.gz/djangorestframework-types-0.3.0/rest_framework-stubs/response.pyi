from typing import Any, Dict, Mapping, Optional

from django.template.response import SimpleTemplateResponse

class Response(SimpleTemplateResponse):
    data: Any
    exception: bool = ...
    content_type: Optional[str] = ...
    _headers: Dict[str, Any]
    def __init__(
        self,
        data: Any = ...,
        status: Optional[int] = ...,
        template_name: Optional[str] = ...,
        headers: Optional[Mapping[str, str]] = ...,
        exception: bool = ...,
        content_type: Optional[str] = ...,
    ): ...
    @property
    def rendered_content(self) -> Any: ...
    @property
    def status_text(self) -> str: ...
