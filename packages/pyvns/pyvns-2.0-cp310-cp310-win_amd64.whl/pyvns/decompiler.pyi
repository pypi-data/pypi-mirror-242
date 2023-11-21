from .content import ContentManager as ContentManager
from .naming import Naming as Naming
from typing import Any

class Decompiler:
    TAG_STARTS: str
    TAG_ENDS: str
    @staticmethod
    def __to_str_in_case_null(text: str | None) -> str: ...
    @classmethod
    def decompile(cls, _data: dict[str, dict[str, dict[str, Any]]], out: str) -> None: ...
