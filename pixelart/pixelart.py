from __future__ import annotations

import dataclasses
import logging
import math

import click
import numpy as np
import vpype as vp
import vpype_cli
from PIL import Image, ImageDraw

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
        cur_dir = (1, 0)
        lines: list[list[complex]] = [[]]

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
                lines[-1].append(cur_pixel.coord())
                cur_dir = (1, 0)

            # try in the current direction first
            next_pixel = cur_pixel.move(cur_dir)
            if next_pixel in pixels:
                cur_pixel = next_pixel
                lines[-1].append(cur_pixel.coord())
                pixels.remove(cur_pixel)
                continue

            # try in all other directions
            for cur_dir in DIRECTIONS - {cur_dir}:
                if (next_pixel := cur_pixel.move(cur_dir)) in pixels:
                    cur_pixel = next_pixel
                    lines[-1].append(cur_pixel.coord())
                    pixels.remove(cur_pixel)
                    break
            else:
                # no connected pixel was found, close the current line
                lines.append([])
                cur_pixel = None

        lc = vp.LineCollection()
        for line in lines:
            if len(line) == 1:
                lc.append([line[0] - 0.1, line[0] + 0.1])
            elif len(line) > 1:
                lc.append(line)
        lc.scale(pen_width)
        document.add(lc, col_idx)


@vpype_cli.cli.command(group="Pixel Art")
@click.argument("image", type=vpype_cli.PathType(exists=True, dir_okay=False))
@click.option("-pw", "--pen-width", type=vpype_cli.LengthType(), default="0.6mm")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(choices=["big", "line", "snake"], case_sensitive=False),
    default="big",
    help="operation mode",
)
@click.option(
    "-u", "--upscale", type=vpype_cli.IntRangeType(min=1), default=1, help="upscale factor."
)
@vpype_cli.global_processor
def pixelart(document: vp.Document, image, mode, pen_width: float, upscale: int):
    """Plot pixel art.

    Three modes are available:
    - "big" creates a square spiral for each pixel
    - "line" create single horizontal lines for contiguous pixels of the same color
    - "snake" tries to traverse contiguous pixels with a single line, using horizontal and
      vertical strokes
    """

    document.add_to_sources(image)

    with Image.open(image) as image_file:
        # noinspection PyTypeChecker
        img = (
            np.array(image_file.convert("RGBA"))
            .repeat(upscale, axis=0)
            .repeat(upscale, axis=1)
        )

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


@vpype_cli.cli.command(group="Pixel Art")
@click.option("-pw", "--pen-width", type=vpype_cli.LengthType(), help="pen width")
@click.option(
    "-m",
    "--mode",
    type=click.Choice(choices=["big", "line", "snake"], case_sensitive=False),
    default="big",
    help="operation mode (same as `pixelart` command)",
)
@click.option("-k", "--keep-lines", is_flag=True, help="Keep the original lines.")
@vpype_cli.layer_processor
def pixelize(layer: vp.LineCollection, pen_width: float | None, mode: str, keep_lines: bool):
    """Turn your vector into pixels, then back into vectors.

    This command creates a bitmap from the geometries, and convert the bitmap back into vector
    using one of the pixelart modes ("big", "line", "snake" -- see `vpype pixelart --help`).

    The pixel size is determined by the layer's current pen width and can be overridden using
    the `--pen-width` option. If undefined, the default pixel size is 0.6mm.

    The original lines are replaced by the pixel-based geometries. Use `--keep-lines` to keep
    them.
    """

    if pen_width is None:
        pen_width = layer.property(vp.METADATA_FIELD_PEN_WIDTH) or vp.convert_length("0.6mm")
    color = layer.property(vp.METADATA_FIELD_COLOR) or vp.Color("black")
    color = color.red, color.green, color.blue

    pixel_pitch = pen_width
    if mode == "big":
        pixel_pitch *= 5

    bounds = layer.bounds()
    if bounds is None:
        logging.warning("!!! pixelize: layer is empty")
        return layer
    x_min, y_min, x_max, y_max = bounds

    img_size = (
        math.ceil((x_max - x_min) / pixel_pitch),
        math.ceil((y_max - y_min) / pixel_pitch),
    )
    img = Image.new("RGBA", img_size)
    draw = ImageDraw.Draw(img)
    for line in layer:
        draw.line(
            [(pt.real, pt.imag) for pt in (line - x_min - 1j * y_min) / pixel_pitch],
            fill=color,
        )

    doc = vp.Document()
    if mode == "big":
        # noinspection PyTypeChecker
        big_mode(doc, np.array(img), np.array([color]), pen_width)
    elif mode == "line":
        # noinspection PyTypeChecker
        line_mode(doc, np.array(img), np.array([color]), pen_width)
    elif mode == "snake":
        # noinspection PyTypeChecker
        snake_mode(doc, np.array(img), np.array([color]), pen_width)

    doc.translate(x_min, y_min)

    if keep_lines:
        layer.extend(doc.layers[1])
        layer.set_property(vp.METADATA_FIELD_PEN_WIDTH, pen_width)
        return layer
    else:
        result = layer.clone(doc.layers[1])
        result.set_property(vp.METADATA_FIELD_PEN_WIDTH, pen_width)
        return result
