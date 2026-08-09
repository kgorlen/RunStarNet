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

import os
import subprocess
import sys
from itertools import count

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
"""Path to directory containing this Python script."""
sys.path.append(str(SCRIPT_DIR))
"""Allow runstarnet CLI to import modules from script directory."""

# pylint: disable=wrong-import-position
from __init__ import __version__  # pylint: disable=no-name-in-module

# pylint: enable=wrong-import-position


def main():
    """Run StarNet on the specified input image."""

    print(f"StarNet Wrapper Version {__version__}")

    if len(sys.argv) != 2:
        print("Usage: python starnet_wrapper.py <input_image>")
        sys.exit(1)

    infile = os.path.abspath(sys.argv[1])

    if not os.path.isfile(infile):
        print(f"Input file not found:\n  {infile}")
        sys.exit(1)

    # Build base output name
    base, ext = os.path.splitext(infile)
    outfile = f"{base}_starless{ext}"

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

    # Handle existing output file
    if os.path.exists(outfile):
        print("Output file already exists:")
        print(f"  {outfile}\n")

        while True:
            choice = (
                input("Choose: (O)verwrite, (N)ew unique file, (A)bort: ")
                .strip()
                .upper()
            )

            if choice == "A":
                sys.exit(1)

            elif choice == "N":
                for i in count(1):
                    candidate = f"{base}_starless_{i}{ext}"
                    if not os.path.exists(candidate):
                        outfile = candidate
                        break
                break

            elif choice == "O":
                break

            else:
                print("Invalid choice. Please enter O, N, or A.")

    # Run StarNet
    cmd = [starnet_exe, "-i", infile, "-o", outfile]

    print("\nRunning:")
    print(" ".join(cmd))
    print()

    result = subprocess.run(cmd, check=False)

    if result.returncode != 0:
        print("StarNet failed.")
        sys.exit(result.returncode)

    print("\nOutput file created:")
    print(f"  {outfile}")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
