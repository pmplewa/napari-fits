# pylint: disable=duplicate-code

from pathlib import Path
from typing import Callable

import pytest
from astropy.io import fits
from napari.layers import Image

from napari_fits._widget import get_fits_reader_widget

from .conftest import SAMPLE_DATA, from_layer_data_tuple


@pytest.mark.parametrize("name", SAMPLE_DATA)
def test_fits_reader_widget(name: str, make_napari_viewer: Callable):
    # pylint: disable=no-value-for-parameter,not-callable
    viewer = make_napari_viewer()

    path = Path(fits.util.get_testdata_filepath(name))
    assert path.is_file()

    widget = get_fits_reader_widget()

    result = widget(path)
    assert len(result) >= 1

    for layer in map(from_layer_data_tuple, result):
        layer = viewer.add_layer(layer)
        assert isinstance(layer, Image)


def test_fits_reader_widget_error():
    # pylint: disable=no-value-for-parameter,not-callable
    widget = get_fits_reader_widget()
    with pytest.raises(FileNotFoundError):
        widget(Path("file.fits"))
