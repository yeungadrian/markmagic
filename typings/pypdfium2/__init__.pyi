"""Stub file for pyright."""

from pathlib import Path
from typing import IO, Any

from pypdfium2._helpers.bitmap import PdfBitmap

class PdfPage:
    def render(
        self,
        scale: float = 1,
        rotation: int = 0,
        crop: tuple[float, float, float, float] = (0, 0, 0, 0),
        may_draw_forms: bool = True,
        bitmap_maker: Any = PdfBitmap.new_native,
        color_scheme: Any | None = None,
        fill_to_stroke: bool = False,
        **kwargs: Any,
    ) -> PdfBitmap: ...

class PdfDocument:
    def __init__(self, input_data: str | Path | bytes | IO[bytes]): ...
    def __len__(self) -> int: ...
    def get_page(self, index: int) -> PdfPage: ...
