"""
Run StarNet on the specified input image.

This script serves as a wrapper around the StarNet CLI so it can be run as an
Additional External Editor from Adobe Lightroom Classic. It checks for existing
output files and prompts the user to choose whether to overwrite, create a new
unique file, or abort the operation.

Usage:
    python starnet_wrapper.py <input_image>

Requirements:
- StarNet CLI must be installed in the default location,
  "C:/Program Files/StarNetv2CLI_Win".

References:
    https://www.starnetastro.com/
"""

__author__ = "Keith Gorlen"

import argparse
import os
import subprocess
import sys
from itertools import count
from pathlib import Path
from typing import NoReturn

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
"""Path to directory containing this Python script."""
sys.path.append(str(SCRIPT_DIR))
"""Allow runstarnet CLI to import modules from script directory."""

# pylint: disable=wrong-import-position
from __init__ import __version__  # pylint: disable=no-name-in-module

# pylint: enable=wrong-import-position

# Global Constants

SCRIPT_NAME: str = os.path.basename(__file__).split(".")[0]
"""Name of this script without .py extension."""

# Global Variables
ARGS: argparse.Namespace
"""Parsed command-line arguments."""


def print_msg(msg: str = "") -> None:
    """Print message if not in quiet mode."""

    if not ARGS.quiet:
        print(msg)


def cleanup_and_exit(status: int = 0) -> NoReturn:
    """Clean up and exit with the given status code."""
    print_msg(f"{SCRIPT_NAME} finished.")
    if ARGS.interactive:
        input("Press Enter to exit ...")

    sys.exit(status)


def fatal_error(msg: str) -> NoReturn:
    """Print a CRITICAL message and sys.exit(1)."""
    print(f"CRITICAL - {msg}; exiting.", file=sys.stderr)
    cleanup_and_exit(1)


def output_files(infile: Path, *outfiles: Path) -> list[Path]:
    """Return output filename list based on the input file name."""

    out_files: list[Path] = list(outfiles)
    """Updated list of output file paths."""

    # Handle existing output file

    for f in out_files:
        if f.exists():
            if ARGS.interactive:
                print(f"Output file already exists:{f}", file=sys.stderr)
            break
    else:
        return out_files  # No output files already exist

    # At least one output file exists
    while True:
        choice = (
            input("Choose: (O)verwrite, (N)ew unique file, (A)bort: ").strip().upper()
            if ARGS.interactive
            else "N"
        )

        if choice == "O":
            break

        elif choice == "N":
            for i in count(1):
                for f in out_files:
                    base, ext = os.path.splitext(f)
                    candidate = f"{base}_{i}{ext}"
                    if os.path.exists(candidate):
                        break
                else:
                    out_files = [
                        Path(f"{os.path.splitext(f)[0]}_{i}{os.path.splitext(f)[1]}")
                        for f in out_files
                    ]
                    return out_files

        elif choice == "A":
            cleanup_and_exit(1)

        else:
            print("Invalid choice. Please enter O, N, or A.", file=sys.stderr)

    return out_files


def prompt_for_options() -> None:
    """Prompt for options in interactive mode."""

    # Prompt for stride until valid or empty (use default)
    while True:
        s = input(
            "Enter stride (384 for wide field, < 256 rarely useful [Standard default 256]: "
        ).strip()
        if not s:
            break
        try:
            sval = int(s)
        except ValueError:
            print("Invalid integer. Please enter an even integer between 2 and 512.")
            continue
        if not (2 <= sval <= 512 and sval % 2 == 0):
            print("Stride must be even and between 2 and 512.")
            continue
        ARGS.stride = sval
        break

    # Prompt for unscreen
    while True:
        u = input("Produce unscreened stars output? (y/n) [n]: ").strip().lower()
        if u in ("y", "yes"):
            ARGS.unscreen = True
            break
        if u in ("n", "no", ""):
            ARGS.unscreen = False
            break
        print("Please enter 'y' or 'n'.")

    # Prompt for upsampling
    while True:
        u = input("Use intermediate 2× upsampling? (y/n) [n]: ").strip().lower()
        if u in ("y", "yes"):
            ARGS.upsample = True
            break
        if u in ("n", "no", ""):
            ARGS.upsample = False
            break
        print("Please enter 'y' or 'n'.")


def main():
    """Run StarNet on the specified input image."""

    parser = argparse.ArgumentParser(description="Run StarNet on an input image")
    parser.add_argument(
        "-i",
        "--interactive",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Prompt for stride, unscreen, and upsample options, default --interactive",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Suppress non-error output, default --noquiet",
    )
    parser.add_argument(
        "-s",
        "--stride",
        type=int,
        default=0,
        help="Tile spacing (even integer between 2 and 512), starnet default if not specified",
    )
    parser.add_argument(
        "-u",
        "--unscreen",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Produce unscreened stars output, default --no-unscreen",
    )
    parser.add_argument(
        "--upsample",
        dest="upsample",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Use intermediate 2× upsampling, default --no-upsample",
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("input", type=Path, nargs=1, help="TIFF or PNG image input file")

    global ARGS
    ARGS = parser.parse_args()

    print_msg(f"StarNet Wrapper Version {__version__}")

    input_path: Path = ARGS.input[0].resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if input_path.suffix.lower() not in (".tif", ".tiff", ".png"):
        raise ValueError("Input must be a TIFF or PNG file.")

    # Get path to StarNet CLI directory
    if sys.platform == "win32":
        starnet_exe = os.path.join(
            os.environ.get("PROGRAMFILES", r"C:\\Program Files"),
            "StarNet2",
            "bin",
            "starnet2.exe",
        )
    elif sys.platform == "darwin":
        # Default for macOS, adjust if StarNet is installed elsewhere
        starnet_exe = "/usr/local/bin/starnet2"
    else:
        starnet_exe = "/usr/bin"

    if not os.path.isfile(starnet_exe):
        print(f"StarNet executable not found:\n  {starnet_exe}")
        sys.exit(1)

    if ARGS.interactive:
        prompt_for_options()

    # Build candidate output filenames
    workdir: Path = input_path.parent
    stem: str = input_path.stem
    suffix: str = input_path.suffix
    nostar_file: Path = workdir / f"{stem}_starless{suffix}"
    """Path to the starless output file."""
    stars_file: Path = workdir / f"{stem}_stars{suffix}"
    """Path to the stars-only output file."""
    unscreened_file: Path = workdir / f"{stem}_unscreened{suffix}"
    """Path to the unscreened stars-only output file."""

    nostar_file, unscreened_file, stars_file = output_files(
        input_path, nostar_file, unscreened_file, stars_file
    )

    # Run StarNet
    cmd = (
        [starnet_exe, "-i", str(input_path), "-o", str(nostar_file)]
        + (["--stride", str(ARGS.stride)] if ARGS.stride else [])
        + (["--upsample"] if ARGS.upsample else [])
        + (["-q"] if ARGS.quiet else [])
    )
    cmd.extend(["-n", str(unscreened_file)] if ARGS.unscreen else ["-m", str(stars_file)])

    print_msg(f"Running: {' '.join(cmd)} ...")
    subprocess.run(cmd, check=True)


def cli() -> None:
    """Command-line interface."""
    try:
        main()
        cleanup_and_exit(0)

    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        sys.exit(1)

    except Exception as e:  # noqa: BLE001
        fatal_error(str(e))


if __name__ == "__main__":
    cli()
