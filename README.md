# vpype-pixelart

[_vpype_](https://github.com/abey79/vpype) plug-in to plot pixel art.

## Usage

### Convert pixelart image to vectors

The `pixelart` command takes an image file as input and converts it to lines according to one of three modes (`big`, `line`, and `small` – see examples below). Each unique color in the the input file results in a new layer created. Pixels which are 100% transparent (alpha = 0) yield no output.

Example invocation:

```bash
$ vpype pixelart --mode snake --pen-width .35mm input.png linesort write output.svg
```

Inline help:

```bash
$ vpype pixelart --help
```

### Convert geometries to bitmaps and back to vector

The `pixelize` command rasterizes the current geometries into a bitmap, and converts them back to vectors similarly to the `pixelart` command.

Example invocation:

```bash
$ vpype read input.svg pixelize --mode snake --pen-width .35mm linesort write output.svg
```

Inline help:

```bash
$ vpype pixelize --help
```


## Examples

### Mode `big`

In this mode, each pixel is drawn using a 5x5 square spiral. The pixel pitch is thus five times the specified pen width.

Cactus sprites from [Super Mario World](https://en.wikipedia.org/wiki/Super_Mario_World):

<img src="https://i.imgur.com/uRhAOJv.png" alt="cactus">

Result plotted with Pentel Sign Pen (using `--pen-width 0.6mm`):

<img src="https://i.imgur.com/pMLkdvG.jpg" alt="big mode plotted pixelart" width=300>

### Mode `line`

In this mode, horizontal lines are generated for horizontal sequences of same-color pixels. The pixel pitch is equal to the specified pen width. 

Original art by [Reddit](https://www.reddit.com/) user [u/\_NoMansDream](https://www.reddit.com/user/_NoMansDream/):

<img src="https://i.redd.it/g1nv7tf20aw11.png" alt="pixel art by u/_NoMansDream" width=600>

Result plotted with Pentel Sign Pen (using `--pen-width 0.6mm`):

<img src="https://i.imgur.com/dAPqFGV.jpg" alt="line mode plotted pixelart" width=600>


### Mode `snake`

In this mode, [snake](https://en.wikipedia.org/wiki/Snake_(video_game_genre)-like lines attempt to traverse zones of contiguous, same-color pixels. Again, the pixel pitch is equal to the specified pen width.

Detail of the snake algoritm:

<img width="600" alt="image" src="https://user-images.githubusercontent.com/49431240/163547592-0714d103-b27d-4ba9-a148-a26213523697.png">

Result plotted with Pentel Sign Pen (using `--pen-width 0.5mm`):

![vpype banner in MacPaint UX](https://user-images.githubusercontent.com/49431240/163547460-49c6e68d-11ed-4aff-a935-6e663bff4a8d.jpeg)


### `pixelize` command

Series of cubes created with [vpype-perspective](https://github.com/abey79/vpype-perspective) and pixelated using `pixelize`:

<img width="600" alt="image" src="https://user-images.githubusercontent.com/49431240/165774053-d29ad6b4-a82c-4d9b-bab7-cd73e827f351.jpeg">



## Installation

See _vpype_'s [installation instructions](https://vpype.readthedocs.io/en/latest/install.html) for information on how to install _vpype_.

### Existing _vpype_ installation

If *vpype* was installed using pipx, use the following command:

```bash
$ pipx inject vpype vpype-pixelart
```

If *vpype* was installed using pip in a virtual environment, activate the virtual environment and use the following command:

```bash
$ pip install vpype-pixelart
```

Check that your install is successful:

```
$ vpype --help
Usage: vpype [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  -v, --verbose
  -I, --include PATH  Load commands from a command file.
  --help              Show this message and exit.

Commands:
[...]
  Plugins:
    pixelart   Plot pixel art.
[...]
```

### Stand-alone installation

Use this method if you need to edit this project. First, clone the project:

```bash
$ git clone https://github.com/abey79/vpype-pixelart.git
$ cd vpype-pixelart
```

Create a virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
```

Install _vpype-pixelart_ and its dependencies (including _vpype_):

```bash
$ pip install -e .
```

Check that your install is successful:

```
$ vpype --help
Usage: vpype [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  -v, --verbose
  -I, --include PATH  Load commands from a command file.
  --help              Show this message and exit.

Commands:
[...]
  Plugins:
    pixelart   Plot pixel art.
[...]
```

## License

See the [LICENSE](LICENSE) file for details.
