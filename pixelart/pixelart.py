import pathlib

import click
import imageio
import numpy as np
import vpype as vp
import vpype_cli

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
@click.argument("image", type=vpype_cli.PathType(exists=True, dir_okay=False))
@click.option("-pw", "--pen-width", type=vpype_cli.LengthType(), default="0.6mm")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(choices=["big", "line"], case_sensitive=False),
    default="big",
    help="operation mode",
)
@vpype_cli.global_processor
def pixelart(document: vp.Document, image, mode, pen_width: float):
    """Plot pixel art.

    Two modes are available:
    - "big" creates a square spiral for each pixel
    - "line" create single horizontal lines for contiguous pixels of the same color
    """

    # this should be dealt with by add_to_source() in a future release
    document.set_property(vp.METADATA_FIELD_SOURCE, pathlib.Path(image).absolute())
    document.add_to_sources(image)

    img = imageio.imread(image, pilmode="RGBA")
    colors = np.unique(img[:, :, 0:3][img[:, :, 3] == 255], axis=0)

    if mode == "big":
        for col_idx, color in enumerate(colors, start=1):
            indice_i, indice_j = np.nonzero(
                np.all(img[:, :, 0:3] == color, axis=2) & (img[:, :, 3] == 255)
            )

            lines = []
            for i, j in zip(indice_j, indice_i):
                line = np.array(PIXEL_TRAJECTORY) + i * PIXEL_OFFSET + j * PIXEL_OFFSET * 1j
                line *= pen_width

                lines.append(line)

            document.add(vp.LineCollection(lines), col_idx)
    elif mode == "line":
        for row_idx, line in enumerate(img):
            start = 0
            while True:
                while start < len(line) and line[start, 3] != 255:
                    start += 1

                # loop ending condition
                if start == len(line):
                    break

                # find the end of the current pixel run
                end = start
                while (
                    end < len(line)
                    and np.all(line[end, 0:3] == line[start, 0:3])
                    and line[end, 3] == 255
                ):
                    end += 1

                #
                layer_id = np.where(np.all(colors == line[start, 0:3], axis=1))[0][0] + 1
                segment = np.array([row_idx * 1j + (start - 0.1), row_idx * 1j + (end - 0.9)])
                segment *= pen_width
                document.add(vp.LineCollection([segment]), layer_id)

                # move to the next line
                start = end

    for col_idx, color in enumerate(colors, start=1):
        document.layers[col_idx].set_property(vp.METADATA_FIELD_COLOR, vp.Color(*color))
        document.layers[col_idx].set_property(vp.METADATA_FIELD_PEN_WIDTH, pen_width)

    return document


pixelart.help_group = "Plugins"
