from ._processor import Processor as Processor
from ._version import REVISION as REVISION, VERSION as VERSION
from typing import Any

class Compiler:
    @staticmethod
    def load(path: str) -> dict[str, Any]: ...
    @classmethod
    def compile(cls, path: str, out_dir: str | None = ...) -> None: ...
    @staticmethod
    def _save(_data: dict[str, Any], _dir: str) -> None: ...
