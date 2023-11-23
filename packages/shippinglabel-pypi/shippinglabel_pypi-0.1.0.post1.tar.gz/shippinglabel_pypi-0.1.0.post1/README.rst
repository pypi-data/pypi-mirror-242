===================
shippinglabel-pypi
===================

.. start short_desc

**Shippinglabel extension for interacting with PyPI.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/domdfcoding/shippinglabel-pypi/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/shippinglabel-pypi/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/shippinglabel-pypi/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/shippinglabel-pypi/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/shippinglabel-pypi/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/shippinglabel-pypi/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/shippinglabel-pypi/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/shippinglabel-pypi/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/shippinglabel-pypi/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/shippinglabel-pypi/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/domdfcoding/shippinglabel-pypi/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/domdfcoding/shippinglabel-pypi/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/shippinglabel-pypi/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/shippinglabel-pypi?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/shippinglabel-pypi?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/shippinglabel-pypi
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/shippinglabel-pypi
	:target: https://pypi.org/project/shippinglabel-pypi/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/shippinglabel-pypi?logo=python&logoColor=white
	:target: https://pypi.org/project/shippinglabel-pypi/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/shippinglabel-pypi
	:target: https://pypi.org/project/shippinglabel-pypi/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/shippinglabel-pypi
	:target: https://pypi.org/project/shippinglabel-pypi/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/shippinglabel-pypi?logo=anaconda
	:target: https://anaconda.org/domdfcoding/shippinglabel-pypi
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/shippinglabel-pypi?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/shippinglabel-pypi
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/domdfcoding/shippinglabel-pypi
	:target: https://github.com/domdfcoding/shippinglabel-pypi/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/shippinglabel-pypi
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/shippinglabel-pypi/v0.1.0.post1
	:target: https://github.com/domdfcoding/shippinglabel-pypi/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/shippinglabel-pypi
	:target: https://github.com/domdfcoding/shippinglabel-pypi/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2023
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/shippinglabel-pypi
	:target: https://pypi.org/project/shippinglabel-pypi/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``shippinglabel-pypi`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install shippinglabel-pypi

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels https://conda.anaconda.org/conda-forge
		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install shippinglabel-pypi

.. end installation
