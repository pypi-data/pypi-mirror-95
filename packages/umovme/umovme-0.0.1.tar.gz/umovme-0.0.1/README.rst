========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-umovme/badge/?style=flat
    :target: https://readthedocs.org/projects/python-umovme
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/kmee/python-umovme.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/kmee/python-umovme

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/kmee/python-umovme?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/kmee/python-umovme

.. |requires| image:: https://requires.io/github/kmee/python-umovme/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/kmee/python-umovme/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/kmee/python-umovme/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/kmee/python-umovme

.. |version| image:: https://img.shields.io/pypi/v/umovme.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/umovme

.. |wheel| image:: https://img.shields.io/pypi/wheel/umovme.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/umovme

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/umovme.svg
    :alt: Supported versions
    :target: https://pypi.org/project/umovme

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/umovme.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/umovme

.. |commits-since| image:: https://img.shields.io/github/commits-since/kmee/python-umovme/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/kmee/python-umovme/compare/v0.0.0...master



.. end-badges

Umovme Api Python Client

* Free software: MIT license

Installation
============

::

    pip install umovme

You can also install the in-development version with::

    pip install https://github.com/kmee/python-umovme/archive/master.zip


Documentation
=============


https://python-umovme.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
