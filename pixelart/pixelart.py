import logging

import numpy as np
import click
import imageio
from vpype import LengthType, LineCollection, Document, global_processor

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
@click.option("--pen-width", type=LengthType(), default="0.6mm")
@click.option(
    "--mode", type=click.Choice(choices=["big", "line"], case_sensitive=False), default="big"
)
@global_processor
def pixelart(document: Document, image, mode, pen_width: float):
    """Plot pixel art"""

    img = imageio.imread(image, pilmode="LA")
    colors = np.unique(img[:, :, 0][img[:, :, 1] == 255])

    if mode == "big":
        for col_idx, color in enumerate(colors):
            indice_i, indice_j = np.nonzero((img[:, :, 0] == color) & (img[:, :, 1] == 255))

            lines = []
            for i, j in zip(indice_j, indice_i):
                line = np.array(PIXEL_TRAJECTORY) + i * PIXEL_OFFSET + j * PIXEL_OFFSET * 1j
                line *= pen_width

                lines.append(line)

            document.add(LineCollection(lines), col_idx + 1)
    elif mode == "line":
        for row_idx, line in enumerate(img):
            start = 0
            while True:
                while start < len(line) and line[start, 1] != 255:
                    start += 1

                # loop ending condition
                if start == len(line):
                    break

                # find the end of the current pixel run
                end = start
                while (
                    end < len(line) and line[end, 0] == line[start, 0] and line[end, 1] == 255
                ):
                    end += 1

                #
                layer_id = np.where(colors == line[start, 0])[0][0] + 1
                segment = np.array([row_idx * 1j + (start - 0.1), row_idx * 1j + (end - 0.9)])
                segment *= pen_width
                document.add(LineCollection([segment]), layer_id)

                # move to the next line
                start = end

    else:
        logging.warning(f"pixelart: unknown mode {mode}, no geometry generated")

    return document


pixelart.help_group = "Plugins"
