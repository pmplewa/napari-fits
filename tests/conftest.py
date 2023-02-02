from napari.layers import Image
from napari.types import LayerDataTuple

SAMPLE_DATA = ["test0.fits", "test1.fits"]


def from_layer_data_tuple(data: LayerDataTuple) -> Image:
    layer_data, layer_params, layer_type = data

    if layer_type == "image":
        return Image(layer_data, **layer_params)

    raise RuntimeError("Unexpected layer type.")
