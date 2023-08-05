########################
pytest-mypy-plugin-shim
########################

.. start short_desc

**Substitute for "pytest-mypy-plugins" for Python implementations which aren't supported by mypy.**

.. end short_desc

See https://github.com/TypedDjango/pytest-mypy-plugins for the action pytest plugin.


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/domdfcoding/pytest-mypy-plugins-shim/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/pytest-mypy-plugins-shim/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/pytest-mypy-plugins-shim/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/pytest-mypy-plugins-shim/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/pytest-mypy-plugins-shim/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/pytest-mypy-plugins-shim/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/pytest-mypy-plugins-shim/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/pytest-mypy-plugins-shim/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/pytest-mypy-plugins-shim/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/pytest-mypy-plugins-shim/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/domdfcoding/pytest-mypy-plugins-shim/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/pytest-mypy-plugins-shim/requirements/?branch=master
	:alt: Requirements Status

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/pytest-mypy-plugins-shim?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/pytest-mypy-plugins-shim
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/pytest-mypy-plugins-shim
	:target: https://pypi.org/project/pytest-mypy-plugins-shim/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pytest-mypy-plugins-shim?logo=python&logoColor=white
	:target: https://pypi.org/project/pytest-mypy-plugins-shim/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pytest-mypy-plugins-shim
	:target: https://pypi.org/project/pytest-mypy-plugins-shim/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/pytest-mypy-plugins-shim
	:target: https://pypi.org/project/pytest-mypy-plugins-shim/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/pytest-mypy-plugins-shim
	:target: https://github.com/domdfcoding/pytest-mypy-plugins-shim/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/pytest-mypy-plugins-shim
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/pytest-mypy-plugins-shim/v0.1.0
	:target: https://github.com/domdfcoding/pytest-mypy-plugins-shim/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/pytest-mypy-plugins-shim
	:target: https://github.com/domdfcoding/pytest-mypy-plugins-shim/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/pytest-mypy-plugins-shim
	:target: https://pypi.org/project/pytest-mypy-plugins-shim/
	:alt: PyPI - Downloads

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/pytest-mypy-plugins-shim/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/pytest-mypy-plugins-shim/master
	:alt: pre-commit.ci status

.. end shields

Installation
--------------

.. start installation

``pytest-mypy-plugins-shim`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install pytest-mypy-plugins-shim

.. end installation
