==============================
SkyAlmanac Project Description
==============================

This is the **PyPI edition** of `SkyAlmanac-Py3 <https://github.com/aendie/Skyalmanac-Py3>`_. Version numbering starts from 1.0 as the previous well-tested SkyAlmanac-Py3 versions that are on github were never published.

Skyalmanac is a **Python 3** script that creates the daily pages of the Nautical Almanac. These are tables that are needed for celestial navigation with a sextant. Although you are strongly advised to purchase the official Nautical Almanac, this program will reproduce the tables with no warranty or guarantee of accuracy.

Skyalmanac uses the star database in Skyfield, which is based on data from the Hipparcos Catalogue. Ephem is used for calculating twilight (actual, civil and nautical sunrise/sunset) and moonrise/moonset. As a consequence, it is four times faster than SFalmanac (which uses Skyfield for almost everything).

Software Requirements
=====================

.. |nbsp| unicode:: 0xA0 
   :trim:

| Most of the computation is done by the free Ephem and Skyfield libraries.
| Typesetting is done typically by MiKTeX or TeX Live.
| These need to be installed:

* Python v3.4 or higher (the latest version is recommended)
* Skyfield >= v1.15 (see the Skyfield Changelog)
* Pandas (to load the Hipparcos catalog; tested: 1.0.3 and 1.1.4)
* Ephem >= 3.7.6
* MiKTeX |nbsp| |nbsp| or |nbsp| |nbsp| TeX Live

Installation
============

Install a TeX/LaTeX program on your operating system so that 'pdflatex' is available.

Ensure that the `pip Python installer tool <https://pip.pypa.io/en/latest/installing.html>`_ is installed. 
Then ensure that old versions of PyEphem, Ephem and Skyalmanac are not installed before installing SkyAlmanac from PyPI::

  python -m pip uninstall pyephem ephem skyalmanac
  python -m pip install skyalmanac

Installing SkyAlmanac ensures that Ephem, Skyfield and Pandas (and their dependencies) are also installed. If previous versions of Skyalmanac were installed, consider upgrading Skyfield and Pandas::

  python -m pip install --upgrade skyfield pandas

Thereafter run it with::

  python -m skyalmanac

On a POSIX system (Linux or Mac OS), use ``python3`` instead of ``python`` above.

This PyPI edition also supports installing and running in a `venv <https://docs.python.org/3/library/venv.html>`_ virtual environment.
Finally check or change the settings in ``config.py``.
It's location is printed immediately whenever Pyalmanac runs.

Guidelines for Linux & Mac OS
-----------------------------

Quote from `Chris Johnson <https://stackoverflow.com/users/763269/chris-johnson>`_:

It's best to not use the system-provided Python directly. Leave that one alone since the OS can change it in undesired ways.

The best practice is to configure your own Python version(s) and manage them on a per-project basis using ``venv`` (for Python 3). This eliminates all dependency on the system-provided Python version, and also isolates each project from other projects on the machine.

Each project can have a different Python point version if needed, and gets its own site_packages directory so pip-installed libraries can also have different versions by project. This approach is a major problem-avoider.

Troubleshooting
---------------

If using MiKTeX 21 or higher, executing 'option 5' (Increments and Corrections) it will probably fail with::

    ! TeX capacity exceeded, sorry [main memory size=3000000].

To resolve this problem (assuming MiKTeX has been installed for all users),
open a Command Prompt as Administrator and enter: ::

    initexmf --admin --edit-config-file=pdflatex

This opens pdflatex.ini in Notepad. Add the following line: ::

    extra_mem_top = 1000000

and save the file. Problem solved. For more details look `here <https://tex.stackexchange.com/questions/438902/how-to-increase-memory-size-for-xelatex-in-miktex/438911#438911>`_.