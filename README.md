# Run StarNet

Run StartNet from Lightroom Classic.

## Overview

This script serves as a wrapper around the StarNet CLI so it can be run as an
Additional External Editor from Adobe Lightroom Classic. It checks for existing
output files and prompts the user to choose whether to overwrite, create a new
unique file, or abort the operation.

## INSTALL StarNet

See [StarNet official page](https://www.starnetastro.com/)

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

Edit -> Preferences -> External Editing -> Additional External Editor:

Preset: Starnet
Application: runstarnet.exe
File Format: TIFF
Template: Filename

## Usage

```sh
runstarnet <input_image>
```

## Requirements

- Python 3.12 or newer

## Project Structure

- [`src/runstarnet/runstarnet.py`](src/runstarnet/runstarnet.py): Main implementation
- [`src/runstarnet/__init__.py`](src/runstarnet/__init__.py): Package metadata

## License

MIT License. See [LICENSE.txt](LICENSE.txt) for details.

## See Also

- [StarNet official page](https://www.starnetastro.com/)

## Author

Keith Gorlen (<kgorlen@gmail.com>)
