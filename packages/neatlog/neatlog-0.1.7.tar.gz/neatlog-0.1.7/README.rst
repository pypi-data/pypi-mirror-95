.. image:: https://img.shields.io/pypi/v/neatlog?style=flat-square
   :target: https://pypi.org/project/neatlog/
   :alt: PyPI

.. image:: https://img.shields.io/pypi/l/neatlog?style=flat-square
   :target: https://gitlab.com/szs/neatlog/-/raw/master/LICENSE
   :alt: PyPI - License

.. image:: https://img.shields.io/pypi/pyversions/neatlog?style=flat-square
   :target: https://python.org
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/gitlab/pipeline/szs/neatlog?style=flat-square
   :target: https://gitlab.com/szs/neatlog/-/pipelines
   :alt: Gitlab pipeline status

.. image:: https://gitlab.com/szs/neatlog/badges/master/coverage.svg?style=flat-square
   :target: https://gitlab.com/szs/neatlog/-/pipelines
   :alt: Coverage

.. image:: https://readthedocs.org/projects/neatlog/badge/?version=latest
   :target: https://neatlog.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


neatlog: A neat logging configuration
=====================================

This package provides an easy and transparent way of customizing the builtin logging.
Just import the module and enjoy the difference.

Installation
============

The installation is straight forward. You can install the package via ``pip``, ``pipenv``, ``poetry``
and alike or by downloading the source from the gitlab repository.

From pypi.org (recommended)
---------------------------

Install by typing

.. code-block:: shell

                pip install neatlog

or

.. code-block:: shell

                pip install --user neatlog

if you do not have root access.

Please check the documentations for `pipenv <https://pipenv.pypa.io/en/latest/>`_, and
`poetry <https://python-poetry.org/docs/>`_ for information on how to install packages with these tools.

From gitlab.com (for experts)
-----------------------------

To get the latest features or contribute to the development, you can clone the whole project using
`git <https://git-scm.com/>`_:

.. code-block:: shell

                git clone https://gitlab.com/szs/neatlog.git


Usage
=====

Simply import neatlog in your program and use logging as usually:

.. code-block:: python

                import logging
                from log_fmt import set_log_level

                set_log_level(logging.DEBUG)
                logging.critical("something critical")
                logging.error("some error")
                logging.warning("some warning")
                logging.info("some info")
                logging.debug("something for debugging")

How to Contribute
=================

If you find a bug, want to propose a feature or need help getting this package to work with your data
on your system, please don't hesitate to file an `issue <https://gitlab.com/szs/neatlog/-/issues>`_ or write
an email. Merge requests are also much appreciated!

Project links
=============

* `Repository <https://gitlab.com/szs/neatlog>`_
* `Documentation <https://neatlog.readthedocs.io/en/latest/>`_
* `pypi page <https://pypi.org/project/neatlog/>`_
