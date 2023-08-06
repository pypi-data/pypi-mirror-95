# Testing

Testing is performed using tox.

## If on a system with a display

Simply running `tox` will take care of everything.

All unittests will be run for each version of Python (3.7, 3.8, 3.9)
available on the system. It will also perform linting with flake8, and
type-checking with mypy.

## If on a system without a display

Some of the unittests are closer to integration tests because they
do not test sections in isolation. Most of these require a GUI to be
able to be drawn, which is not possible on a system without a display.

In such cases, these tests must unfortunately be left out due to the
limitations of the source code.

Some test environments are already set up for such cases. Running
`tox -e 'py3{7,8,9}'-nodisplay',flake,mypy` will do everything
that a plain `tox` commmand will do, except it will leave out the
tests that require a GUI.

This is especially useful for CI where testing is performed in a Docker
container.
