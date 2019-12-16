import numpy as np
import click
import imageio
from vpype.utils import Length
from vpype.model import LineCollection, VectorData
from vpype.decorators import global_processor

# normalized spiral trajectory for a single pixel
# units are in pen width
PIXEL_TRAJECTORY = [
    0,
    1j,
    -1 + 1j,
    -1 - 1j,
    1 - 1j,
    1 + 2j,
    -2 + 2j,
    -2 - 2j,
    2 - 2j,
    2 + 2j,
]

PIXEL_OFFSET = 5


@click.command()
@click.argument("image", type=click.Path(exists=True, dir_okay=False))
@click.option("--pen-width", type=Length())
@global_processor
def pixelart(vector_data: VectorData, image, pen_width: float):
    """
    Insert documentation here.
    """

    img = imageio.imread(image, pilmode="LA")
    colors = np.unique(img[:, :, 0][img[:, :, 1] == 255])

    for col_idx, color in enumerate(colors):
        indice_i, indice_j = np.nonzero((img[:, :, 0] == color) & (img[:, :, 1] == 255))

        lines = []
        for i, j in zip(indice_j, indice_i):
            line = np.array(PIXEL_TRAJECTORY) + i * PIXEL_OFFSET + j * PIXEL_OFFSET * 1j
            line *= pen_width

            lines.append(line)

        vector_data.add(LineCollection(lines), col_idx + 1)

    return vector_data


pixelart.help_group = "Plugins"
