from __future__ import annotations

import dataclasses

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


def big_mode(document: vp.Document, img: np.ndarray, colors: np.ndarray, pen_width: float):
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


def line_mode(document: vp.Document, img: np.ndarray, colors: np.ndarray, pen_width: float):
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


DIRECTIONS = frozenset(((1, 0), (-1, 0), (0, 1), (0, -1)))


@dataclasses.dataclass(frozen=True)
class Pixel:
    x: int = 0
    y: int = 0

    def move(self, direction: tuple[int, int]) -> Pixel:
        return Pixel(self.x + direction[0], self.y + direction[1])

    def coord(self) -> complex:
        return self.x + 1j * self.y


def snake_mode(document: vp.Document, img: np.ndarray, colors: np.ndarray, pen_width: float):
    for col_idx, color in enumerate(colors, start=1):
        pixels = {
            Pixel(x, y)
            for y, x in np.argwhere(
                np.all(img[:, :, 0:3] == color, axis=2) & (img[:, :, 3] == 255)
            )
        }

        cur_pixel: Pixel | None = None
        cur_line: list[complex] = list([])
        cur_dir = (1, 0)
        lc = vp.LineCollection()

        while pixels:
            if cur_pixel is None:
                # pick a random pixel
                for cur_pixel in pixels:
                    break

                # try to move as far up/left in that pixel black as possible
                while {
                    up := cur_pixel.move((0, -1)),
                    left := cur_pixel.move((-1, 0)),
                } & pixels:
                    if up in pixels:
                        cur_pixel = up
                    else:
                        cur_pixel = left

                pixels.remove(cur_pixel)
                cur_line = [cur_pixel.coord()]
                cur_dir = (1, 0)

            # try in the current direction first
            next_pixel = cur_pixel.move(cur_dir)
            if next_pixel in pixels:
                cur_pixel = next_pixel
                cur_line.append(cur_pixel.coord())
                pixels.remove(cur_pixel)
                continue

            # try in all other directions
            for cur_dir in DIRECTIONS - {cur_dir}:
                if (next_pixel := cur_pixel.move(cur_dir)) in pixels:
                    cur_pixel = next_pixel
                    cur_line.append(cur_pixel.coord())
                    pixels.remove(cur_pixel)
                    break
            else:
                # no connected pixel was found, close the current line
                if len(cur_line) == 1:
                    cur_line = [cur_line[0] - 0.1, cur_line[0] + 0.1]
                lc.append(cur_line)
                cur_pixel = None

        lc.scale(pen_width)
        document.add(lc, col_idx)


@click.command()
@click.argument("image", type=vpype_cli.PathType(exists=True, dir_okay=False))
@click.option("-pw", "--pen-width", type=vpype_cli.LengthType(), default="0.6mm")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(choices=["big", "line", "snake"], case_sensitive=False),
    default="big",
    help="operation mode",
)
@vpype_cli.global_processor
def pixelart(document: vp.Document, image, mode, pen_width: float):
    """Plot pixel art.

    Three modes are available:
    - "big" creates a square spiral for each pixel
    - "line" create single horizontal lines for contiguous pixels of the same color
    - "snake" tries to traverse contiguous pixels with a single line, using horizontal and
      vertical strokes
    """

    document.add_to_sources(image)

    img = imageio.imread(image, pilmode="RGBA")
    colors = np.unique(img[:, :, 0:3][img[:, :, 3] == 255], axis=0)

    if mode == "big":
        big_mode(document, img, colors, pen_width)
    elif mode == "line":
        line_mode(document, img, colors, pen_width)
    elif mode == "snake":
        snake_mode(document, img, colors, pen_width)

    for col_idx, color in enumerate(colors, start=1):
        document.layers[col_idx].set_property(vp.METADATA_FIELD_COLOR, vp.Color(*color))
        document.layers[col_idx].set_property(vp.METADATA_FIELD_PEN_WIDTH, pen_width)

    return document


pixelart.help_group = "Plugins"
