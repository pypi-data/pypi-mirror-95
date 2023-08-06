# Installation

This is geared towards those who intend to develop this application.

## Why

This package must be installed in order for tests to work properly.
In an uninstalled state, cross-package imports break because packages
have no way to recognize each other. By installing, the top-level
directory is added to sys.path and each package is recognized.

## How

1. Get the distribution by either cloning this repository or
downloading the source through pip and untaring.
2. Set up and activate a virtual environment.
3. Install in editable mode with `pip -e .` in the same directory as
setup.py. With an editable install, changes in the codebase show up
immediately in the installed package.
