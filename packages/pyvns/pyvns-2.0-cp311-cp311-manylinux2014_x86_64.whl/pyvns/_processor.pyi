from ._exception import ScriptCompilerException as ScriptCompilerException
from .content import Content as Content
from .naming import Naming as Naming
from _typeshed import Incomplete
from typing import Any, Final, NoReturn

class Processor:
    SCRIPTS_FILE_EXTENSION: Final[str]
    __ALTERNATIVES: dict[str, str]
    __RESERVED_WORDS: tuple[str, ...]
    TAG_STARTS: str
    TAG_ENDS: str
    __path_in: str
    __line_index: int
    __output: Incomplete
    __current_data: Incomplete
    __id: int
    __lang: str
    __section: str
    __previous: Incomplete
    __lines: Incomplete
    __dialog_associate_key: Incomplete
    __accumulated_comments: Incomplete
    __blocked: bool
    def __init__(self) -> None: ...
    def get_id(self) -> int: ...
    def get_language(self) -> str: ...
    @staticmethod
    def __ensure_not_null(text: str) -> str | None: ...
    @classmethod
    def __extract_parameter(cls, text: str) -> str | None: ...
    @classmethod
    def __extract_tag(cls, text: str) -> str: ...
    @classmethod
    def __extract_string(cls, text: str) -> str: ...
    def __terminated(self, _reason: str) -> NoReturn: ...
    def __get_current_line(self) -> str: ...
    def get_output(self) -> dict[str, dict[str, dict[str, Any]]]: ...
    def process(self, _path: str) -> None: ...
    def __convert(self, staring_index: int) -> None: ...
