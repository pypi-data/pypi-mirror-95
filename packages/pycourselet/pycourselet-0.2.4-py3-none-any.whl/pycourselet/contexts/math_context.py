from typing import Optional

from .context import NeedSettings
from .enumerate_context import EnumerateContext
from .text_context import TextContext


class MathTextContext(TextContext):
    def __init__(self, mode: str = 'tex', **kwargs):
        super().__init__(type='math', **kwargs)
        self.mode = mode

    @staticmethod
    def need() -> Optional[NeedSettings]:
        from .paragraph_context import ParagraphContext
        from .table_contexts import TableBlockContext

        return NeedSettings(ParagraphContext, TableBlockContext, EnumerateContext)
