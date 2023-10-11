from pathlib import Path
from typing import Callable, Iterator, Sequence, cast

import dask.array as da
from astropy.io import fits
from napari.types import LayerDataTuple


def get_fits_reader(path: str | Sequence[str]) -> Callable | None:
    if not isinstance(path, str):
        return None

    if Path(path).suffix != ".fits":
        return None

    return read_fits


def _read_fits(path: str | Path, *, memmap: bool = False) -> Iterator[LayerDataTuple]:
    hdul = fits.open(path, memmap=memmap)

    for hdu in hdul:
        if not hdu.is_image:
            continue

        if hdu.data is None:
            continue

        layer_data = da.from_array(hdu.data)
        layer_params = {"name": hdu.name, "metadata": {"header": hdu.header}}
        layer_type = "image"

        yield cast(LayerDataTuple, (layer_data, layer_params, layer_type))


def read_fits(path: str | Path) -> list[LayerDataTuple]:
    try:
        return list(_read_fits(path, memmap=True))
    except ValueError:
        return list(_read_fits(path, memmap=False))
