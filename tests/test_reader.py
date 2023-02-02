# pylint: disable=duplicate-code

from pathlib import Path
from typing import Callable

import pytest
from astropy.io import fits
from napari.layers import Image

from napari_fits._reader import get_fits_reader, read_fits

from .conftest import SAMPLE_DATA, from_layer_data_tuple


@pytest.mark.parametrize("name", SAMPLE_DATA)
def test_fits_reader(name: str, make_napari_viewer: Callable):
    viewer = make_napari_viewer()

    path = Path(fits.util.get_testdata_filepath(name))
    assert path.is_file()

    reader = get_fits_reader(str(path))
    assert callable(reader)
    # pylint: disable-next=comparison-with-callable
    assert reader == read_fits

    result = reader(path)
    assert len(result) >= 1

    for layer in map(from_layer_data_tuple, result):
        layer = viewer.add_layer(layer)
        assert isinstance(layer, Image)


def test_fits_reader_pass():
    assert get_fits_reader(["file_1.fits", "file_2.fits"]) is None
    assert get_fits_reader("file.txt") is None
