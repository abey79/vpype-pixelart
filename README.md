# vpype-pixelart

[_vpype_](https://github.com/abey79/vpype) plug-in to plot pixel art.


## Examples

### `big` mode

Cactus sprites from [Super Mario World](https://en.wikipedia.org/wiki/Super_Mario_World):

<img src="https://i.imgur.com/uRhAOJv.png" alt="cactus">

Result plotted with Pentel Sign Pen (using `--pen-width 0.6mm`):

<img src="https://i.imgur.com/pMLkdvG.jpg" alt="big mode plotted pixelart" width=300>

### `line` mode

Original art by [Reddit](https://www.reddit.com/) user [u/\_NoMansDream](https://www.reddit.com/user/_NoMansDream/):

<img src="https://i.redd.it/g1nv7tf20aw11.png" alt="pixel art by u/_NoMansDream" width=600>

Result plotted with Pentel Sign Pen (using `--pen-width 0.6mm`):

<img src="https://i.imgur.com/dAPqFGV.jpg" alt="line mode plotted pixelart" width=600>


## Installation

See _vpype_'s [installation instructions](https://github.com/abey79/vpype/blob/master/INSTALL.md) for information on how to install _vpype_.

### Existing _vpype_ installation

Use this method if you have an existing _vpype_ installation (typically in an existing virtual environment) and you want to make this plug-in available. You must activate your virtual environment beforehand.

*IMPORTANT*: the `feature-plugins` branch of _vpype_ must temporarily be used, until it is merged back into `master`.

```bash
$ pip install git+https://github.com/abey79/vpype-pixelart.git#egg=vpype-pixelart
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


## Documentation

The complete plug-in documentation is available directly in the CLI help:

```bash
$ vpype pixelart --help
```


## License

See the [LICENSE](LICENSE) file for details.
