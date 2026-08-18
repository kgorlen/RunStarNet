<!--
Markdown Guide: https://www.markdownguide.org/basic-syntax/
-->
<!--
Disable markdownlint errors:
fenced-code-language MD040
no-inline-html MD033
-->
<!-- markdownlint-disable MD040 MD033-->

# Run StarNet

Run StartNet v2 from Lightroom Classic or as a command.

## Overview

This script serves as a wrapper around the StarNet CLI so it can be run as an
Additional External Editor from Adobe Lightroom Classic or as a command. It
prompts for StarNet options and also checks for existing output files, prompting
to choose whether to overwrite, create a new unique files, or abort.

Produces **two** output files:

- *input_image*_starless.tif
- *input_image*_stars.tif if **--no-unscreen** specified (default), suitable for blending with the starless image in *Linear Dodge (Add)* mode, **OR**
- *input_image*_unscreen.tif if **--unscreen** specified, suitable for blending with the starless image in *Screen* mode.

_*n* is appended to the filename if any output file exists and *New* is selected
when prompted.  *New* is assumed if **--no-interactive**.

## INSTALL Python

See [Python](https://www.python.org/downloads/).

## INSTALL pipx

See [pipx](https://pypi.org/project/pipx/).

## INSTALL StarNet

See [StarNet official page](https://www.starnetastro.com/).

## INSTALL **runstarnet** FROM `.whl` package

<pre>
<code>pipx install <i>path</i>\runstarnet-<i>version</i>-py3-none-any.whl</code>
</pre>

For example:

<pre>
<code>pipx install <i>path</i>\runstarnet-1.0.1-py3-none-any.whl</code>
</pre>

## INSTALL **runstarnet** FROM `.tar.gz` package

Alternatively, install **runstarnet** from a `.tar.gz` package file:

<pre>
<code>pipx install <i>path</i>\runstarnet-<i>version</i>.tar.gz</code>
</pre>

For example:

<pre>
<code>pipx install <i>path</i>\runstarnet-1.0.1-.tar.gz</code>
</pre>

## Configure Adobe Lightroom Classic

*Edit -> Preferences -> External Editing -> Additional External Editor*:

Preset: Starnet
Application: runstarnet.exe
File Format: TIFF
Template: Filename

## Usage

**runstarnet** [**-h**] [**-i** | **--interactive** | **--no-interactive**] [**-q** | **--quiet**
| **--no-quiet**] [**-s** *STRIDE*] [**-u** | **--unscreen** | **--no-unscreen**] [**--upsample** |
**--no-upsample**] *infile*

### Positional arguments

*infile*
:   Input TIFF or PNG image file

### Options

**-h, --help**
:   show this help message and exit

**-i, --interactive, --no-interactive**
:   Prompt for stride, unscreen, and upsample options, default --interactive

**-q, --quiet, --no-quiet**
:   Suppress non-error output, default --noquiet

**-s STRIDE, --stride STRIDE**
:   Tile spacing (even integer between 2 and 512)

**-u, --unscreen, --no-unscreen**
:   Produce unscreened stars output, default --no-unscreen

**--upsample, --no-upsample**
:   Use intermediate 2× upsampling, default --no-upsample

## Requirements

- Python 3.12 or newer

## License

MIT License. See [LICENSE.txt](LICENSE.txt) for details.

## See Also

- [StarNet official page](https://www.starnetastro.com/)

## Author

Keith Gorlen (<kgorlen@gmail.com>)
