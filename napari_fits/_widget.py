from pathlib import Path

from magicgui import magic_factory
from napari.types import LayerDataTuple

from ._reader import read_fits


@magic_factory(
    call_button="Load",
    path={"label": "Path", "tooltip": "The file path.", "mode": "r"},
)
def get_fits_reader_widget(path: Path) -> list[LayerDataTuple]:
    if not path.is_file():
        raise FileNotFoundError(path)

    return read_fits(path)
